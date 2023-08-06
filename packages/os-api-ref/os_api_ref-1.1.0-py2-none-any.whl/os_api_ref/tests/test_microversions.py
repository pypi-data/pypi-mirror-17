# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
test_os_api_ref
----------------------------------

Tests for `os_api_ref` module.
"""

from bs4 import BeautifulSoup
from sphinx_testing import with_app

from os_api_ref.tests import base


class TestMicroversions(base.TestCase):
    """Test basic rendering.

    This can be used to test that basic rendering works for these
    examples, so if someone breaks something we know.
    """

    @with_app(buildername='html', srcdir=base.example_dir('microversions'),
              copy_srcdir_to_tmpdir=True)
    def setUp(self, app, status, warning):
        super(TestMicroversions, self).setUp()
        self.app = app
        self.app.build()
        self.status = status.getvalue()
        self.warning = warning.getvalue()
        self.html = (app.outdir / 'index.html').read_text()
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.content = str(self.soup)

    def test_rest_method(self):
        """Test that min / max mv css class attributes are set"""
        content = self.soup.find_all(class_='rp_min_ver_2_17')
        self.assertIn(
            '<div class="operation-grp rp_min_ver_2_17 rp_max_ver_2_19 ">',
            str(content[0]))
        content = self.soup.find_all(class_='rp_max_ver_2_19')
        self.assertIn(
            '<div class="operation-grp rp_min_ver_2_17 rp_max_ver_2_19 ">',
            str(content[0]))

    def test_parameters_table(self):
        """Test that min / max mv css class attributes are set in params"""
        table = """<div class="api-detail collapse section" id="list-servers-detail">
<table border="1" class="docutils">
<colgroup>
<col width="20%"></col>
<col width="10%"></col>
<col width="10%"></col>
<col width="60%"></col>
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">Name</th>
<th class="head">In</th>
<th class="head">Type</th>
<th class="head">Description</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-even"><td>name</td>
<td>body</td>
<td>string</td>
<td>The name of things</td>
</tr>
<tr class="rp_min_ver_2_11 row-odd"><td>name2</td>
<td>body</td>
<td>string</td>
<td><p class="first">The name of things</p>
<p class="last"><strong>New in version 2.11</strong></p>
</td>
</tr>
<tr class="rp_max_ver_2_20 row-even"><td>name3</td>
<td>body</td>
<td>string</td>
<td><p class="first">The name of things</p>
<p class="last"><strong>Deprecated in version 2.20</strong></p>
</td>
</tr>
</tbody>
</table>
</div>
"""  # noqa
        self.assertIn(table, self.content)

    def test_mv_selector(self):

        button_selectors = \
            """<div aria-label="..." class="btn-group" role="group">
<button class="btn btn-default mv_selector active" type="button">All</button>
<button class="btn btn-default mv_selector" type="button">2.1</button>
<button class="btn btn-default mv_selector" type="button">2.2</button>
<button class="btn btn-default mv_selector" type="button">2.3</button>
<button class="btn btn-default mv_selector" type="button">2.4</button>
<button class="btn btn-default mv_selector" type="button">2.5</button>
<button class="btn btn-default mv_selector" type="button">2.6</button>
<button class="btn btn-default mv_selector" type="button">2.7</button>
<button class="btn btn-default mv_selector" type="button">2.8</button>
<button class="btn btn-default mv_selector" type="button">2.9</button>
<button class="btn btn-default mv_selector" type="button">2.10</button>
<button class="btn btn-default mv_selector" type="button">2.11</button>
<button class="btn btn-default mv_selector" type="button">2.12</button>
<button class="btn btn-default mv_selector" type="button">2.13</button>
<button class="btn btn-default mv_selector" type="button">2.14</button>
<button class="btn btn-default mv_selector" type="button">2.15</button>
<button class="btn btn-default mv_selector" type="button">2.16</button>
<button class="btn btn-default mv_selector" type="button">2.17</button>
<button class="btn btn-default mv_selector" type="button">2.18</button>
<button class="btn btn-default mv_selector" type="button">2.19</button>
<button class="btn btn-default mv_selector" type="button">2.20</button>
<button class="btn btn-default mv_selector" type="button">2.21</button>
<button class="btn btn-default mv_selector" type="button">2.22</button>
<button class="btn btn-default mv_selector" type="button">2.23</button>
<button class="btn btn-default mv_selector" type="button">2.24</button>
<button class="btn btn-default mv_selector" type="button">2.25</button>
<button class="btn btn-default mv_selector" type="button">2.26</button>
<button class="btn btn-default mv_selector" type="button">2.27</button>
<button class="btn btn-default mv_selector" type="button">2.28</button>
<button class="btn btn-default mv_selector" type="button">2.29</button>
<button class="btn btn-default mv_selector" type="button">2.30</button>
</div>"""
        self.assertIn(button_selectors, self.content)

    def test_js_declares(self):
        self.assertIn("os_max_mv = 30;", self.content)
        self.assertIn("os_min_mv = 1;", self.content)
