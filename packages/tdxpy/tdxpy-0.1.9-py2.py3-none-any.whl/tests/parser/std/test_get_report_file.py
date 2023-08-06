from tdxpy.hq import TdxHq_API


def test_get_report_file():
    api = TdxHq_API()

    with api.connect(ip="120.76.152.87"):
        content = api.get_report_file_by_size("tdxfin/gpcw.txt")

        assert len(content) > 0
        assert content
