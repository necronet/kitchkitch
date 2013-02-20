from base import BaseTest
import json

class TableTest(BaseTest):
    def setUp(self):
        super(TableTest, self).setUp('/table/',auth=True)

    def test_post(self):
        rv=self.post(data=json.dumps({"name":"#1"}))
        print rv.data
        assert rv.status_code == 201