import pandas as pd

from tdxpy.crawler.base_crawler import fetch_report_hook
from tdxpy.crawler.history_financial_crawler import HistoryFinancialCrawler
from tdxpy.crawler.history_financial_crawler import HistoryFinancialListCrawler


def test_history_financial_crawler():
    crawler = HistoryFinancialListCrawler()
    list_data = crawler.fetch_and_parse(reporthook=fetch_report_hook)
    df = pd.DataFrame(data=list_data)

    assert df.empty is False

    assert df["filename"].str.contains("gpcw20190630.zip").any()

    filename = list_data[1]["filename"]
    filesize = list_data[1]["filesize"]
    print(filename, filesize)

    datacrawler = HistoryFinancialCrawler()
    pd.set_option("display.max_columns", None)
    result = datacrawler.fetch_and_parse(reporthook=fetch_report_hook, filename=filename, filesize=filesize, path_to_download="/tmp/gpcw20190630.zip")
    print(result)

    with open(r"/tmp/gpcw20190630.zip", "rb") as fp:
        result = datacrawler.parse(download_file=fp)
        print(datacrawler.to_df(data=result))
