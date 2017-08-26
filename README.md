# scrapy\_proxy\_crawler

基于scrapy的代理IP爬虫

## 解决什么问题

使用代理是一种常见的应对封锁IP等反爬虫措施的反反爬虫措施. 

国内有数家提供免费代理IP的网站, 但是多数免费代理都是没法使用的, 每天更新的可用代理不过数十, 若是手工挑选, 未免太过繁琐. 故实现此爬虫, 用于批量爬取代理, 并在爬取过程中自行检查可用性. 

仅基于scrapy实现, 没有其他依赖, 方便用于基于scrapy的爬虫.

## 代理来源
	
 - 西刺代理 
 - 66ip 
 - 快代理

## 依赖

 - Scrapy 1.4.0 (更老的版本没测试过)

## 使用 
	
### 运行

一如启动普通scrapy爬虫一般:

	scrapy crawl proxy_spider

其接收来自命令行的参数: `proxy_check_url`和`max_need_proxy`:

  - `proxy_check_url`用于检查代理ip是否可用, 默认是`https//www.baidu.com`, 使用时可换成你的目标网址
  - `max_need_proxy`用于限制获取代理ip的个数, 默认是100, 检查可用的代理ip达到`max_need_proxy`时, 爬虫会自动停止.

这两个参数都可以在settings.py中配置: `PROXY_CHECK_URL`和`MAX_NEED_PROXY`.

运行过程中可能打印大量Error和Traceback, 这是因为检查代理可用性时, 代理不可用导致的, 属正常现象.

### 保存代理地址

检查可用的代理, 会构造为`scrapy_proxy_crawler.items.ProxyItem`, `addr`是ProxyItem的唯一的Field, 其格式为`http://ip:port`, 您需要自行编写ItemPipeline来处理这些ProxyItem.

## 最后

这其实是某次帮人写爬虫时留下的代码, 当时需求简单, 只保存了`ip:port`, 其余信息如地区, 是否匿名, 是不是https一概没管, 功能确实挺简陋的, 以后有时间再改进吧, 各位有需求提issue便是.