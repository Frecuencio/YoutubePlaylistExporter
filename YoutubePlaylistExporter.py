#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pytube import YouTube
from pytube import Playlist
from pytube.exceptions import VideoUnavailable
from pytube.exceptions import VideoPrivate
from datetime import date
import time
import csv
import argparse
from sys import exit


class PlaylistSaver(object):
	def __init__(self, playlist, pname, pdate, gencsv, genhtml, genurl, csvdelimiter, csvquote, sleep, download):
		super(PlaylistSaver, self).__init__()
		self.playlist = playlist
		self.pname = pname
		self.pdate = pdate
		self.gencsv = gencsv
		self.genhtml = genhtml
		self.genurl = genurl
		self.csvdelimiter = csvdelimiter
		self.csvquote = csvquote
		self.sleep = sleep
		self.download = download

	def savePlaylist(self):
		self.playlist = Playlist("https://www.youtube.com/playlist?list=%s" % self.playlist)
		self.fname = self.playlist.title
		print(u'Loaded playlist %s\nNumber of videos in playlist: %s' % (self.fname, len(self.playlist.video_urls)))
		# Custom name, change saved variable
		if self.pname:
			self.fname = self.pname
		# Prepend date
		if self.pdate:
			self.fname += date.today().strftime("%Y%m%d")

		if self.genhtml:
			self.saveHTML()

		# CSV generator can download videos
		if self.gencsv:
			self.saveCSV()

		# If CSV not generated, but video downlaod is asked
		if self.download and not self.gencsv:
			self.downloadVideos()

		if self.genurl:
			self.saveUrlTxt()
		return

	def saveHTML(self):
		print("-- Generating HTML --")
		htmlfile = open("%s.html" % self.fname, "w", encoding="utf-8")
		htmlfile.write(u"%s" % self.playlist.html)
		htmlfile.close()
		print(u"--Saved %s.html--" % self.fname)

	def saveCSV(self):
		print("-- Creating CSV --")
		with open("%s.csv" % self.fname, 'w', newline='\n', encoding="utf-8") as csvfile:
				videowriter = csv.writer(csvfile, delimiter=self.csvdelimiter,quotechar=self.csvquote, quoting=csv.QUOTE_ALL)
				videowriter.writerow(['name','url','author','publish_date','length','description','keywords'])
				for videourl in self.playlist.video_urls:
					try:
						video = YouTube(videourl)
						videowriter.writerow([video.title,video.watch_url,video.author,video.publish_date,video.length,video.description,video.keywords])
						print(u"Saved into csv: %s" % video.title)
						if self.download:
							print(u"Downloading: %s" % video.title)
							video.streams.first().download()
						time.sleep(self.sleep)
					except VideoPrivate:
						print("Skipped: Private Video")
						continue
					except VideoUnavailable:
						print("Skipped: Video Unavailable")
						continue
					except KeyboardInterrupt:
						exit()
					except:
						print("Skipped: Other exception")
						continue
		print("--Saved %s.csv--" % self.fname)

	def downloadVideos(self):
		print("-- Downloading videos --")
		for videourl in self.playlist.video_urls:
			try:
				video = YouTube(videourl)
				print(u"Downloading: %s" % video.title)
				video.streams.first().download()
			except VideoPrivate:
				print("Skipped: Private Video")
				continue
			except VideoUnavailable:
				print("Skipped: Video Unavailable")
				continue
			except KeyboardInterrupt:
				exit()
			except:
				print("Skipped: Other exception")
				continue

	def saveUrlTxt(self):
		print("-- Creating TXT --")
		urlfile = open("%s.txt" % self.fname, "w")
		for videourl in self.playlist.video_urls:
			urlfile.write("%s\n" % videourl)
		urlfile.close()
		print(u"--Saved %s.txt--" % self.fname)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Backup Youtube playlist into CSV, html and/or txt file.')
	parser.add_argument('-pl', '--playlist', required=True, help='Playlist ID', type=str)
	parser.add_argument('-n', '--name', required=False, help='Generated filename (name+date if not -nd present). Playlist name used if not specified', type=str)
	parser.add_argument('-nd', '--nodate', required=False, help='Don\'t prepend date on filename', action='store_false', default=True)
	parser.add_argument('-nc', '--nocsv', required=False, help='Don\'t generate CSV file', action='store_false', default=True)
	parser.add_argument('-d', '--delimiter', required=False, help='Delimiter used in CSV file (Default= , )', default=',')
	parser.add_argument('-q', '--quotechar', required=False, help='Quote character used in CSV file (Default= | )', default='|')
	parser.add_argument('-u', '--urlfile', required=False, help='Generate TXT with only urls', action='store_false', default=True)
	parser.add_argument('-html', '--html', required=False, help='Generate HTML file', action='store_true', default=False)
	parser.add_argument('-w', '--wait', required=False, help='Wait specified seconds between videos, useful if you get HTTP Error 429: Too Many Requests', default=0, type=int)
	parser.add_argument('-dl', '--download', required=False, help='Automatic download all the videos',action='store_true', default=False)


	args = parser.parse_args()

	start_time = time.time()
	pl = PlaylistSaver(args.playlist, args.name, args.nodate, args.nocsv, args.html, args.urlfile, args.delimiter, args.quotechar, args.wait, args.download)
	pl.savePlaylist()

	totaltime = time.time() - start_time
	print(" --- Total time spent: %s seconds (%s mins) ---" % (totaltime, totaltime/60))
