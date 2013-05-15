##
# Copyright (c) 2006-2013 Apple Inc. All rights reserved.
# Copyright (c) 2013 Sriram Karra <karra.etc@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

from caldavclientlibrary.protocol.webdav.session import Session
from caldavclientlibrary.protocol.carddav.multiget import Multiget
from StringIO import StringIO
from caldavclientlibrary.protocol.url import URL
from caldavclientlibrary.protocol.webdav.definitions import davxml
from caldavclientlibrary.protocol.carddav.definitions import carddavxml
from caldavclientlibrary.client.account import CalDAVAccount
import unittest

host = 'localhost:8443'
ssl  = True

class TestRequest(unittest.TestCase):


    def test_Method(self):

        server = Session(host)
        request = Multiget(server, "/", ())
        self.assertEqual(request.getMethod(), "REPORT")



class TestRequestHeaders(unittest.TestCase):
    pass



class TestRequestBody(unittest.TestCase):

    def test_GenerateXMLOneHrefOnly(self):

        server = Session(host)
        request = Multiget(server, "/", ("/a",))
        os = StringIO()
        request.generateXML(os)
        self.assertEqual(os.getvalue(), """<?xml version='1.0' encoding='utf-8'?>
<ns0:addressbook-multiget xmlns:ns0="urn:ietf:params:xml:ns:carddav">
  <ns1:href xmlns:ns1="DAV:">/a</ns1:href>
</ns0:addressbook-multiget>
""".replace("\n", "\r\n")
)


    def test_GenerateXMLMultipleHrefsOnly(self):

        server = Session(host)
        request = Multiget(server, "/", ("/a", "/b",))
        os = StringIO()
        request.generateXML(os)
        self.assertEqual(os.getvalue(), """<?xml version='1.0' encoding='utf-8'?>
<ns0:addressbook-multiget xmlns:ns0="urn:ietf:params:xml:ns:carddav">
  <ns1:href xmlns:ns1="DAV:">/a</ns1:href>
  <ns1:href xmlns:ns1="DAV:">/b</ns1:href>
</ns0:addressbook-multiget>
""".replace("\n", "\r\n")
)


    def test_GenerateXMLMultipleHrefsOneProperty(self):

        server = Session(host)
        request = Multiget(server, "/", ("/a", "/b",), (davxml.getetag,))
        os = StringIO()
        request.generateXML(os)
        self.assertEqual(os.getvalue(), """<?xml version='1.0' encoding='utf-8'?>
<ns0:addressbook-multiget xmlns:ns0="urn:ietf:params:xml:ns:carddav">
  <ns1:prop xmlns:ns1="DAV:">
    <ns1:getetag />
  </ns1:prop>
  <ns1:href xmlns:ns1="DAV:">/a</ns1:href>
  <ns1:href xmlns:ns1="DAV:">/b</ns1:href>
</ns0:addressbook-multiget>
""".replace("\n", "\r\n")
)


    def test_GenerateXMLMultipleHrefsMultipleProperties(self):

        server = Session(host)
        request = Multiget(server, "/", ("/a", "/b",), (davxml.getetag, davxml.displayname,))
        os = StringIO()
        request.generateXML(os)
        self.assertEqual(os.getvalue(), """<?xml version='1.0' encoding='utf-8'?>
<ns0:addressbook-multiget xmlns:ns0="urn:ietf:params:xml:ns:carddav">
  <ns1:prop xmlns:ns1="DAV:">
    <ns1:getetag />
    <ns1:displayname />
  </ns1:prop>
  <ns1:href xmlns:ns1="DAV:">/a</ns1:href>
  <ns1:href xmlns:ns1="DAV:">/b</ns1:href>
</ns0:addressbook-multiget>
""".replace("\n", "\r\n")
)



class TestResponse(unittest.TestCase):

    ## FIXME: These tests need to be adapted to specific installations and
    ## settings. A better approach would be to install a setUp() method that
    ## would PUT some of these resources at a given root, and then try to
    ## multiget... Too much effort for now, but at a later point. maybe.

    @classmethod
    def setUpClass(self):

        self.acc = CalDAVAccount(host, ssl=ssl, user=raw_input('Username: '),
                                 pswd=raw_input('Password: '), logging=False)
        self.root = "/addressbooks/__uids__/skarrag/addressbook/"
        hrefs = (self.root + "395dc187673076cdba17557d12f94ce5.vcf",
                 self.root + "7d69f2f10edb55e9ec15f99cdd321b88.vcf",
                 self.root + "8afb07c99deac51532a10a4070aa48ec.vcf")

        self.request = Multiget(self.acc.session,  self.root, hrefs=hrefs,
                                props=(davxml.getetag, davxml.displayname,
                                       carddavxml.address_data,))

        self.acc.session.runSession(self.request)


    def test_ResponseStatus(self):

        self.assertEqual(self.request.getStatusCode(), 207)

    def test_ResponseHeaders(self):

        hdrs = self.request.getResponseHeaders()



class TestResponseHeaders(unittest.TestCase):
    pass



class TestResponseBody(unittest.TestCase):
    pass


def main (argv=None):
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRequest)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestRequestBody)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestResponse)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()
