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
import re
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

def get_author(post):
    return post.find("div", "post_username").find("span", {"class": "author vcard"}).text.strip()

def format_text(comment):
    comment = comment.replace('\n', ' ').replace('\t', ' ').strip()
    return re.sub(r'\s+', ' ', comment)

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
                    comment_list = soup.findAll("div", {"class": "post_body"})
                    if page == "page-1.html":
                        post_title = soup.head.title.text.strip()
                        original_post = comment_list[0]
                        author = get_author(original_post)
                        page_url = thread_url + "/#"

                        thread_writer.writerow({"Thread ID": thread_id, "Thread Link": page_url, "Market": market, "Vendor Name": author, "Product/Service Name": post_title, "Replies": "MANUAL", "Views": "MANUAL", "Category": category, "Price": "MANUAL", "Unit": "MANUAL", "Payment Method": "MANUAL"})
                    else:
                        page_url = thread_url + "/" + page[:-5]

                    for comment in comment_list:
                        comment_number = comment.find("span", {"class": "post_id"}).a.text.strip()[1:]
                        commenter = get_author(comment)
                        post_text = format_text(comment.find("section").text) # need to format, look into str.replace('\n', '')
                        #print(post_text)
                        comment_writer.writerow({"Thread ID": thread_id, "Comment Link": page_url, "Floor Number": comment_number, "Username": commenter, "Trade": "0", "Review": "0", "Q&A": "0", "Content": post_text})
            thread_id += 1
