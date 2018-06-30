# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from up_work_spider.settings import FILE_RESULT, BOT_NAME


class JsonWriterPipeline(object):

    result_file = BOT_NAME + '/' + FILE_RESULT

    def open_spider(self, spider):

        self.file = open(file=self.result_file, mode='r')

        # create task_ID set
        self.id_list = list()
        for line in self.file.readlines():
            # print('---1st LINE', line)
            url_id = json.loads(line).get('url_to_project')
            self.id_list.append(url_id)
        # print('id_list', self.id_list)

        self.file.close()

        self.file = open(file=self.result_file, mode='a')

    def process_item(self, item, spider):

        json_obj = dict(item)

        # add rows that are not in the id_list
        if json_obj.get('url_to_project') not in list(set(self.id_list)):
            line = json.dumps(json_obj, sort_keys=True) + "\n"
            self.file.write(line)

    def close_spider(self, spider):
        self.file.close()  # close after crawl
