#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

class PrinterController(appier.Controller):

    @appier.route("/printers.json", "GET", json = True)
    def list(self):
        return self.npcolony.get_devices()

    @appier.route("/printers/hello.json", "GET", json = True)
    def hello(self):
        self.npcolony.print_hello()

    @appier.route("/printers/<str:printer>/print.json", ("GET", "POST"), json = True)
    def print_document(self, printer):
        data_b64 = self.field("data_b64")
        self.npcolony.print_printer_base64(printer, data_b64)

    @property
    def npcolony(self):
        import npcolony
        return npcolony
