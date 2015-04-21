#!/usr/bin/env python3
import os
from gi.repository import Gtk, GObject
from subprocess import Popen, check_output, call, PIPE
from sys import argv
from tempfile import NamedTemporaryFile

class ProgressBarWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Converting to PDF...")
        self.set_border_width(10)
        self.set_default_size(400,100)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.progressbar = Gtk.ProgressBar()
        vbox.pack_start(self.progressbar, True, False, 0)
        self.timeout_id = GObject.timeout_add(80, self.on_timeout)

        #self.tmpfile = check_output(['mktemp', '-p', '/tmp', 'pdfconv_XXXXXX.pdf'])
        #print(self.tmpfile)
        #self.tmpfile = mkstemp(suffix='.pdf', prefix='pdfconv_', dir='/tmp')
        #tmpfile = NamedTemporaryFile(suffix='.pdf', prefix='pdfconv_', dir='/tmp') 
        self.unoconv_thread = Popen(['unoconv', '--stdout', argv[1]], stdout=tmpfile.file)
        #print(self.tmpfile)
        #self.tmpfile.file.open()
        #self.unoconv_thread.stdout = self.tmpfile.file
        #self.add(self.progressbar)
    def on_timeout (self):
        self.progressbar.pulse()
        if self.unoconv_thread.poll() is not None:
            GObject.source_remove(self.timeout_id)
            #self.tmpfile.file.flush()
            #self.tmpfile.file.close()
            #os.fsync(self.tmpfile.file)
            #self.destroy()
            self.hide()

            Gtk.main_quit()
            #call(['evince', self.tmpfile.name])
            #os.unlink(self.tmpfile.name)
            #Gtk.main_quit()
        return True
tmpfile = NamedTemporaryFile(suffix='.pdf', prefix='pdfconv_', dir='/tmp') 
win = ProgressBarWindow()
win.connect("delete-event", Gtk.main_quit)
#win.progressbar.pulse()
win.show_all()
Gtk.main()
call(['evince', tmpfile.name])
os.unlink(tmpfile.name)
#Gtk.main_quit()
