#!/usr/bin/python3
# Copyright 2017 Virgil Dupras
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

# import sys
# import os.path as op
# import gc

# from PyQt5.QtCore import QCoreApplication, QSettings
# from PyQt5.QtGui import QIcon, QPixmap
# from PyQt5.QtWidgets import QApplication

# from hscommon.trans import install_gettext_trans_under_qt
# from qtlib.error_report_dialog import install_excepthook
# from qtlib.util import setupQtLogging
# from qt import dg_rc
# from qt.platform import BASE_PATH
from core import engine, fs, directories
# from core.gui import result_table

from hscommon.path import Path
from hscommon.jobprogress import job
from hscommon.util import rem_file_ext

# SIGQUIT is not defined on Windows
# if sys.platform == 'win32':
#     from signal import signal, SIGINT, SIGTERM
#     SIGQUIT = SIGTERM
# else:
#from signal import signal, SIGINT, SIGTERM, SIGQUIT

# === INITIALISATION ===
print("\n\n\n\n======= ESOTIM - PIPELINE TEST =======\n\n")
__folderpath__ = "/usr/src/app/CHOMA/"

__fileclasses__ = []
#__fileclasses__ += [fs.Folder]
__fileclasses__ += [fs.File]

key_func = lambda x: -x.size
#tie_breaker = lambda ref, dupe: dupe.bar > ref.bar
tie_breaker = None

csv_del = ','


repertoires = directories.Directories()

def do_progress(p, d=''):
    #print("Log job : " + str(p))
    return True

j = job.Job(10, do_progress)

print("Analysons le répertoire " + __folderpath__ + " ...")


# === AJOUT DES REPERTOIRES ===
print("Ajout du répertoire " + __folderpath__)

try:
    repertoires.add_path(Path(__folderpath__))
except directories.AlreadyThereError:
    print("'{}' est déjà dans la liste.").format(__folderpath__)
except directories.InvalidPathError:
    print("'{}' n'existe pas.").format(__folderpath__)

print("Répertoire " + __folderpath__ + " ajouté !")


# === RÉCUPÉRATION DES FICHIERS DU RÉPERTOIRE ===
print("Récupération des fichiers ...")

files = list(repertoires.get_files(fileclasses=__fileclasses__))

print('%d fichiers récupérés !\n\n' % len(files))

#print(files)

# === RÉCUPÉRATION DES DOUBLONS ===
print("Scan des doublons ...")
j = j.start_subjob([2, 8])

kw = {}
kw['match_similar_words'] = False
kw['weight_words'] = True
kw['min_match_percentage'] = 65
kw['no_field_order'] = True

scan_type = "filename"

func = {
    "filename": lambda f: engine.getwords(rem_file_ext(f.name)),
    "fields": lambda f: engine.getfields(rem_file_ext(f.name)),
    "tag": lambda f: [
        engine.getwords(str(getattr(f, attrname)))
        for attrname in SCANNABLE_TAGS
        if attrname in self.scanned_tags
    ],
}[scan_type]


for f in j.iter_with_progress(files, "Lecture des métadonnées de %d/%d fichiers"):
    print('Lecture des métadonnées de ' + f.name)
    f.words = func(f)

doublons = engine.getmatches(files, j=j, **kw)

print('%d paires de doublons trouvées ! Voici les premiers :\n' % len(doublons))
for i in range(0,min(10,len(doublons))):
    print(str(doublons[i].percentage) + "% de ressemblance :")
    print(doublons[i].first.path)
    print(doublons[i].second.path)

print('\n')

# === GROUPEMENT DES DOUBLONS ===
print('Groupement des doublons...')

groupes = engine.get_groups(doublons)
groupes = [g for g in groupes if any(not f.is_ref for f in g)]

print('%d groupes formés !\n\n' % len(groupes))


# === IMPRESSION DES RESULTATS ===

def surr(s="",i=-1):
    if i >= 0:
        return "\"" + str(i) + "\""
    else:
        return "\"" + s + "\""

def getCSVLine(file, group, is_ref=False):
    res = ""
    res += surr(file.name) + csv_del
    res += surr("Référence" if is_ref else "Doublon") + csv_del
    res += surr(i=file.size) + csv_del
    res += surr(i=len(group)) + csv_del
    res += surr(file.path)

    return res

def getCSVHead():
    res = ""
    res += surr("Nom") + csv_del
    res += surr("Type") + csv_del
    res += surr("Taille") + csv_del
    res += surr("Nombre de doublons") + csv_del
    res += surr("Chemin")

    return res

print(getCSVHead())

for g in groupes:
    g.prioritize(key_func, tie_breaker)
    print(getCSVLine(g.ref, g, True))
    for f in g.dupes:
        print(getCSVLine(f,g, False))


# def getfiles(directories, j):
#     j.set_progress(0, tr("Collecting files to scan"))

#     files = list(directories.get_files(fileclasses=self.fileclasses, j=j))
#     print('Scan de %d fichiers...' % len(files))


# def _getmatches(files, j):
#     j = j.start_subjob([2, 8])

#     scan_type = ScanType.Filename

#     kw = {}
#     kw['match_similar_words'] = False
#     kw['weight_words'] = True
#     kw['min_match_percentage'] = 90
#     kw['no_field_order'] = True

#     func = {
#         ScanType.Filename: lambda f: engine.getwords(rem_file_ext(f.name)),
#         ScanType.Fields: lambda f: engine.getfields(rem_file_ext(f.name)),
#         ScanType.Tag: lambda f: [
#             engine.getwords(str(getattr(f, attrname)))
#             for attrname in SCANNABLE_TAGS
#             if attrname in self.scanned_tags
#         ],
#     }[scan_type]


#     for f in j.iter_with_progress(files, "Lecture des métadonnées de %d/%d fichiers"):
#         logging.debug("Lecture des métadonnées de %s", f.path)
#         f.words = func(f)
#     return engine.getmatches(files, j=j, **kw)


# if self.scan_type == ScanType.Folders and matches:
#             allpath = {m.first.path for m in matches}
#             allpath |= {m.second.path for m in matches}
#             sortedpaths = sorted(allpath)
#             toremove = set()
#             last_parent_path = sortedpaths[0]
#             for p in sortedpaths[1:]:
#                 if p in last_parent_path:
#                     toremove.add(p)
#                 else:
#                     last_parent_path = p
#             matches = [m for m in matches if m.first.path not in toremove or m.second.path not in toremove]
#         if not self.mix_file_kind:
#             matches = [m for m in matches if get_file_ext(m.first.name) == get_file_ext(m.second.name)]
#         matches = [m for m in matches if m.first.path.exists() and m.second.path.exists()]
#         matches = [m for m in matches if not (m.first.is_ref and m.second.is_ref)]
#         if ignore_list:
#             matches = [
#                 m for m in matches
#                 if not ignore_list.AreIgnored(str(m.first.path), str(m.second.path))
#             ]
#         logging.info('Grouping matches')
#         groups = engine.get_groups(matches)
#         if self.scan_type in {ScanType.Filename, ScanType.Fields, ScanType.FieldsNoOrder, ScanType.Tag}:
#             matched_files = dedupe([m.first for m in matches] + [m.second for m in matches])
#             self.discarded_file_count = len(matched_files) - sum(len(g) for g in groups)
#         else:
#             # Ticket #195
#             # To speed up the scan, we don't bother comparing contents of files that are both ref
#             # files. However, this messes up "discarded" counting because there's a missing match
#             # in cases where we end up with a dupe group anyway (with a non-ref file). Because it's
#             # impossible to have discarded matches in exact dupe scans, we simply set it at 0, thus
#             # bypassing our tricky problem.
#             # Also, although ScanType.FuzzyBlock is not always doing exact comparisons, we also
#             # bypass ref comparison, thus messing up with our "discarded" count. So we're
#             # effectively disabling the "discarded" feature in PE, but it's better than falsely
#             # reporting discarded matches.
#             self.discarded_file_count = 0
#         groups = [g for g in groups if any(not f.is_ref for f in g)]
#         logging.info('Created %d groups' % len(groups))
#         for g in groups:
#             g.prioritize(self._key_func, self._tie_breaker)
#         return groups

    # def _get_export_data(self):
    #     columns = [
    #         col for col in self.result_table.columns.ordered_columns
    #         if col.visible and col.name != 'marked'
    #     ]
    #     colnames = [col.display for col in columns]
    #     rows = []
    #     for group_id, group in enumerate(self.results.groups):
    #         for dupe in group:
    #             data = self.get_display_info(dupe, group)
    #             row = [fix_surrogate_encoding(data[col.name]) for col in columns]
    #             row.insert(0, group_id)
    #             rows.append(row)
    #     return colnames, rows

# global dgapp
# dgapp = None

# def signalHandler(sig, frame):
#     global dgapp
#     if dgapp is None:
#         return
#     if sig in (SIGINT, SIGTERM, SIGQUIT):
#         dgapp.SIGTERM.emit()

# def setUpSignals():
#     signal(SIGINT,  signalHandler)
#     signal(SIGTERM, signalHandler)
#     signal(SIGQUIT, signalHandler)

# def main():
    # app = QApplication(sys.argv)
    # QCoreApplication.setOrganizationName('Hardcoded Software')
    # QCoreApplication.setApplicationName(__appname__)
    # QCoreApplication.setApplicationVersion(__version__)
    # setupQtLogging()
    # settings = QSettings()
    # lang = settings.value('Language')
    # locale_folder = op.join(BASE_PATH, 'locale')
    # install_gettext_trans_under_qt(locale_folder, lang)
    # # Handle OS signals
    # setUpSignals()



    # Let the Python interpreter runs every 500ms to handle signals.  This is
    # required because Python cannot handle signals while the Qt event loop is
    # running.

    # from PyQt5.QtCore import QTimer
    # timer = QTimer()
    # timer.start(500)
    # timer.timeout.connect(lambda: None)



    # Many strings are translated at import time, so this is why we only import after the translator
    # has been installed

    # from qt.app import DupeGuru
    # app.setWindowIcon(QIcon(QPixmap(":/{0}".format(DupeGuru.LOGO_NAME))))
    # global dgapp
    # dgapp = DupeGuru()
    # install_excepthook('https://github.com/hsoft/dupeguru/issues')
    # result = app.exec()



    # I was getting weird crashes when quitting under Windows, and manually deleting main app
    # references with gc.collect() in between seems to fix the problem.

    # del dgapp
    # gc.collect()
    # del app
    # gc.collect()
    # return result

# if __name__ == "__main__":
#     sys.exit(main())
