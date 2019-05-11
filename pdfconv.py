#!/usr/bin/env python3
import os
import sys
import select
from subprocess import Popen, call, PIPE, STDOUT
from tempfile import NamedTemporaryFile
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


class PDFConvWindow(Gtk.Window):
    def __init__(self, docfile):
        Gtk.Window.__init__(self, title="Converting to PDF...")
        self.set_border_width(10)
        self.set_default_size(400, 100)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        self.progressbar = Gtk.ProgressBar()
        vbox.pack_start(self.progressbar, True, False, 0)

        self.tmpfile = NamedTemporaryFile(suffix='.pdf', prefix=os.path.basename(docfile) + '.', dir='/tmp', delete=False)
        self.tmpfile.file.close()
        self.process = Popen(['unoconv', '-v', '-o', self.tmpfile.name, docfile], stderr=STDOUT, stdout=PIPE, text=True, bufsize=0)
        self.timeout_id = GLib.timeout_add(80, self.on_timeout)
        self.connect("delete-event", Gtk.main_quit)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.show_all()

    def on_timeout(self):
        self.progressbar.pulse()
        if select.select([self.process.stdout], [], [], .01)[0] != []:
            print(self.process.stdout.read())
        if self.process.poll() is not None:
            self.hide()
            Gtk.main_quit()
            stdout_data, _ = self.process.communicate()
            return False
        return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        win = PDFConvWindow(sys.argv[1])
        Gtk.main()

        if win.process.returncode == 0:
            xdgopen = Popen(['xdg-open', win.tmpfile.name], preexec_fn=os.setsid)
            xdgopen.wait()
    else:
        print("Usage: {cmd} [filename]".format(cmd=sys.argv[0]))
