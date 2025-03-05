#!/usr/bin/env python3

"""
Post publish script after org-publish an org file:
1. Generate index page
2. Generate rss file
"""

from os.path import expanduser, getmtime
from glob import glob
from datetime import datetime

rss_header = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>无名PhD的读书札记</title>
    <link>https://101scholar.github.io</link>
    <description>Scholar 101 的个人读书札记</description>
    <language>zh-cmn-Hans</language>
"""

rss_footer = """  <channel>
</rss>"""

rss_item = """    <item>
      <title>{title}</title>
      <description>{title}</description>
      <author>Scholar 101</author>
      <pubDate>{pub_date}</pubDate>
      <link>https://101scholar.github.io/{fname}</link>
      <guid>https://101scholar.github.io/{fname}</guid>
    </item>"""

index_header = """<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-cmn-Hans" lang="zh-cmn-Hans">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <meta name="description" content="这是 Scholar 101 的个人读书札记。">
    <meta name="author" content="Scholar 101" />
    <title>读书札记 | Scholar 101</title>
    <link rel="stylesheet" href="index.css">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-HV71CP0QWE"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-HV71CP0QWE');
    </script>
  </head>

  <body>
    <div id="container">
      <div id="main" role="main">
        <header>
        <h1><center>读书札记</center></h1>  
        </header>
        
        <blockquote class="homepage">
        <center>
        <em>
        流浪诗人有自己的旅途<br />
        在喧闹的港口，在荒凉的峡谷<br />
        在远离尘嚣的角落<br />
        流浪诗人有自己的歌喉<br />
        在火红的黎明，在温柔的黄昏<br />
        在夜的面前从不沉默<br />
        </em>
        </center>
        </blockquote>
        <section class="meta" style="color: #999999;">我的邮箱：scholar101 点 me 艾特 gmail 点 com</section>

        <article class="content">
          <section class="post">
            <ul class="listing">
"""

index_footer = """            </ul>
          </section>
        </article>
      </div>
    </div>
  </body>
  
  <footer><p><small><center>
    <a href="http://101scholar.github.io/rss.xml" title="RSS 订阅" target="_blank" >RSS</a>
  </center></small></p></footer>
</html>
"""

index_year = """              <li class="listing-seperator">{}</li>
"""
index_item = """              <li class="listing-item">
                <time datetime="{date}">{date}</time>
                <a href="{fname}" title="{title}">{title}</a>
              </li>
"""

li = []
folder = expanduser("~/Dropbox/personal/2-resource/org/writing/output-blog/")
for f in sorted(glob(folder + "*.html"), key=lambda xx: getmtime(xx), reverse=True):
    if not f.endswith("/index.html"):
        title = ""
        with open(f) as infile:
            for line in infile.readlines():
                if "<title>" in line:
                    title = line.replace(
                        "<title>", "").replace(
                        "</title>", "").strip()
        dt = datetime.fromtimestamp(getmtime(f))
        fname = f.split("/")[-1]
        date = dt.strftime("%Y-%m-%d")
        year = dt.strftime("%Y")
        pub_date = dt.strftime("%a, %d %b %Y %H:%M:%S %z +0800")
        li.append(dict(
            title=title, pub_date=pub_date, fname=fname,
            date=date, year=year))

with open(folder + "rss.xml", "w") as outfile:
    print(rss_header, file=outfile)
    for item in li:
        print(rss_item.format(**item), file=outfile)
    print(rss_footer, file=outfile)

with open(folder + "index.html", "w") as outfile:
    print(index_header, file=outfile)
    cur_year = None
    for item in li:
        if item["year"] != cur_year:
            print(index_year.format(item["year"]), file=outfile)
            cur_year = item["year"]
        print(index_item.format(**item), file=outfile)
    print(index_footer, file=outfile)

