#!/usr/bin/env bash

#
# This is a janky little script to reformat the frames api docs. Needs to be redone
#

rm -rf docs/api/frames


# Frames
sphinx-apidoc -efT -o docs/api/frames src/brite_etl/frames src/brite_etl/frames/prepared
for i in docs/api/frames/frames.*; do mv $i ${i/frames./}; done
sed -i -- 's/frames./brite_etl.frames./g' docs/api/frames/*.rst
sed -i -r 's/brite_etl[.]frames[.](.*)\smodule/``\1``/' docs/api/frames/*.rst
# Fix index file
mv docs/api/frames/rst docs/api/frames/index.rst
sed -i -- 's/frames package/``brite_etl.frames``/g' docs/api/frames/index.rst
sed -i -r 's/\sframes.(.*)/\1/g' docs/api/frames/index.rst
# sed -i -- 's/Submodules/Frames/g' docs/api/frames/index.rst
sed -i '/x_report_locations/a \  Prepared Frames <prepared/index>' docs/api/frames/index.rst
sed -i -e '/Module contents/ { N; N; N; N; N; N; d; }' docs/api/frames/index.rst
sed -i -e '/==============/a\\n.. automodule:: brite_etl.frames\n\n   .. contents::\n      :local:\n' docs/api/frames/index.rst
sed -i -- 's/==============/====================/g' docs/api/frames/index.rst




# Prepared Frames
sphinx-apidoc -efT -o docs/api/frames/prepared src/brite_etl/frames/prepared
for i in docs/api/frames/prepared/prepared.*; do mv $i ${i/prepared./}; done
sed -i -- 's/prepared./brite_etl.frames.prepared./g' docs/api/frames/prepared/*.rst
sed -i -r 's/brite_etl[.]frames[.]prepared[.](.*)\smodule/``\1``/' docs/api/frames/prepared/*.rst
# Fix index file
mv docs/api/frames/prepared/rst docs/api/frames/prepared/index.rst
sed -i -- 's/prepared package/``brite_etl.frames.prepared``/g' docs/api/frames/prepared/index.rst
sed -i -r 's/\sprepared.(.*)/\1/g' docs/api/frames/prepared/index.rst
# sed -i -- 's/Submodules/Frames/g' docs/api/frames/prepared/index.rst
sed -i -e '/Module contents/ { N; N; N; N; N; N; d; }' docs/api/frames/prepared/index.rst
sed -i -e '/==============/a\\n.. automodule:: brite_etl.frames.prepared\n\n   .. contents::\n      :local:\n' docs/api/frames/prepared/index.rst
sed -i -- 's/================/=============================/g' docs/api/frames/prepared/index.rst
