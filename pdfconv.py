#!/usr/bin/env python3
import os
from gi.repository import Gtk, GObject
from subprocess import Popen, call, PIPE
from sys import argv
from tempfile import NamedTemporaryFile

class PDFConvWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Converting to PDF...")
        self.set_border_width(10)
        self.set_default_size(400,100)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        self.progressbar = Gtk.ProgressBar()
        vbox.pack_start(self.progressbar, True, False, 0)
        self.timeout_id = GObject.timeout_add(80, self.on_timeout)

        self.tmpfile = NamedTemporaryFile(suffix='.pdf', prefix='pdfconv_', dir='/tmp', delete=False)
        self.tmpfile.file.close()
        self.unoconv_thread = Popen(['unoconv', '-o', self.tmpfile.name, argv[1]])
    def on_timeout (self):
        self.progressbar.pulse()
        if self.unoconv_thread.poll() is not None:
            GObject.source_remove(self.timeout_id)
            self.hide()
            Gtk.main_quit()
        return True

win = PDFConvWindow()
win.connect("delete-event", Gtk.main_quit)
win.set_position(Gtk.WindowPosition.CENTER)
win.show_all()
Gtk.main()
call(['evince', win.tmpfile.name])
os.unlink(win.tmpfile.name)
