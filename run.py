#!/usr/bin/python
import MySQLdb
import re, os
import requests, json

host='localhost'
user='user'
passwd='password'
database='s3dw'

db = MySQLdb.connect(host=host, # your host, usually localhost
                     user=user, # your username
                      passwd=passwd, # your password
                      db=database) # name of the data base


def convert(content, inputFormat, outputFormat):
    payload = {'input':inputFormat,'output':outputFormat,'text':content}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        'User-Agent': 'curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)'
    }
    # Try to convert online
    try:
        r = requests.post("http://marksy.arc90.com/convert", headers=headers, data=json.dumps(payload))
        response = r.json()
        return response['payload']
    except:
        return content

def main():
    # Required folder
    if not os.path.exists('export'):
        os.makedirs('export')

    cur = db.cursor()

    cur.execute("SELECT * FROM forum_node where node_type='question'")
    for row in cur.fetchall() :

        id = row[0]
        title = row[1].replace('/','_')
        filename = re.sub(r"\s+", '_', title)
        tags = row[2]
        question = row[4]
        date_created = row[8].strftime('%Y%m%d%H%M%S') + '000'
        date_modified = row[13].strftime('%Y%m%d%H%M%S') + '000'

        cur2 = db.cursor()
        cur2.execute("SELECT * FROM forum_node where parent_id='%s'" % id)
        content = question + "\n\n"
        for subrow in cur2.fetchall() :
            content += "\n\n" + subrow[4]
        convertedContent = convert(content, "markdown", "mediawiki")
        f = open("export/"+filename+".tid","w")
        f.write("created: " + date_created + "\n")
        f.write("modified: " + date_modified + "\n")
        f.write("tags: " + tags + "\n")
        f.write("title: " + title + "\n")
        f.write("type: text/vnd.tiddlywiki\n")
        f.write("\n")
        try:
            f.write(convertedContent)
        except:
            f.write(content)
        f.close()

if __name__ == "__main__":
        main()
