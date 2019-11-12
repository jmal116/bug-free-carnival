# <div class="post_wrap">
#     <div class="author_info clearfix">
#         <div class="user_details ">
#             <span class="hide" itemprop="name">                   --> commenter name
#     <div class="post_body">
#         <span class="post_id right ipsType_small desc blend_links">
#             <a itemprop="replyToUrl" rel="bookmark">              --> entry no. of form "#1"
#         <div class="post entry-content " itemprop="commentText">
#             <section id="nulledPost">                             --> comment text
    

# <html>
#     <title> --> title of post

import os, sys
import csv
from os.path import isdir, join
from bs4 import BeautifulSoup

data_root_path = os.path.dirname(os.path.abspath(__file__))
base_url = "https://www.nulled.to/topic/"
market = "Nulled"

data_directories = ["CaaS", "crimeware"]

thread_data = "threadData.csv"
thread_fields = ["Thread ID", "Thread Link", "Market", "Vendor Name", "Product/Service Name", "Replies", "Views", "Category", "Price", "Unit", "Payment Method"]

comment_data = "commentData.csv"
comment_fields = ["Thread ID", "Comment Link", "Floor Number", "Username", "Trade", "Review", "Q&A", "Content"]

thread_id = 0

with open(thread_data, 'w') as threads, open(comment_data, 'w') as comments:
    thread_writer = csv.DictWriter(threads, fieldnames=thread_fields)
    thread_writer.writeheader()
    comment_writer = csv.DictWriter(comments, fieldnames=comment_fields)
    comment_writer.writeheader()
    for category in data_directories:
        for thread in os.listdir(join(data_root_path, category)):
            thread_url = base_url + thread
            for page in os.listdir(join(data_root_path, category, thread)):
                with open(join(data_root_path, category, thread, page), 'r') as p:
                    soup = BeautifulSoup(p, "html.parser")
                    if page == "page-1.html":
                        # get product/service name with soup -- <title> tag
                        # get OP by finding the username of the first comment
                        ### soup.findAll(div, {"class": "post_wrap"})[0]
                        page_url = thread_url + "/#"
                        thread_writer.writerow({"Thread ID": thread_id, "Thread Link": page_url, "Market": market, "Vendor Name": "DERIVE", "Product/Service Name": "DERIVE", "Replies": "MANUAL", "Views": "MANUAL", "Category": category, "Price": "MANUAL", "Unit": "MANUAL", "Payment Method": "MANUAL"})
                    else:
                        page_url = thread_url + "/" + page[:-5]
                    comments = [] # use soup.findAll for class="post_wrap"
                    for comment in comments:
                        comment_writer.writerow({"Thread ID": thread_id, "Comment Link": page_url, "Floor Number": "DERIVED", "Username": "DERIVED", "Trade": "MANUAL", "Review": "MANUAL", "Q&A": "MANUAL", "Content": "DERIVED"})
                    pass
            thread_id += 1
