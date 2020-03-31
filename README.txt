小说抓取说明：

一、正常抓取
1、拷贝爬虫模板文件xbiquge/spiders/sancun.py
若在xbiquge网站中，只需要修改爬虫名，小说章节url等参数即可
2、修改pipelines.py文件
需要修改数据库名，小说起始章节url，小说中文名
3、若是其他网站，则需要通过测试，修改对应的items条目内容，具体情况具体分析。

二、抓取单章方法
有时，在抓取小说过程中，会出现个别章节没有成功抓取，若重新全部抓取的话比较费时，考虑抓取单章内容进行补充。
1、修改爬虫文件，模板：xiaoyaoxss1.py （取消爬取目录页的parse函数，直接爬取单页内容）
2、修改pipelines.py, 模板: pipelines1.py  (取消爬虫起始函数，避免重新建表损坏数据表已有内容。注意，pipelines1.py需要修改为pipelines.py才可用。单章抓取完成后，应及时恢复原pipelines.py文件。)
3、运行单章爬取爬虫： scrapy crawl xiaoyaoxss1.py
4、若内容补充完成，需要重新生成txt文件，直接运行spiders2txt.py即可：python spiders2txt.py


