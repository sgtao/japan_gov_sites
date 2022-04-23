#!/bin/sh
# 01_convert_csvfiles_with_cityURLs.sh
#
# function : conver to csvfile_with_cityURLs:
#   with argv[1] = jsonfile
#   with argv[2] = output directory
convert_csvfile_with_cityURLs() {
  csvfile_l=` basename $1 | sed -e "s/\.json/\.csv/"  ` ;
  python3 11_get_wiki_pub_links.py $1;
  /bin/mv outcsv_with_cityURLs.csv $2/$csvfile_l;
  echo "# output to $2/$csvfile_l";
}
#
# start script
CSVDIR='csvfiles'
if [ ! -d $CSVDIR ] ; then
  mkdir $CSVDIR;
fi
#
# for jsonfile in ../docs/assets/3[1-2]_*.json ; do
for jsonfile in ../docs/assets/*.json ; do
  echo "convert $jsonfile";
  convert_csvfile_with_cityURLs $jsonfile $CSVDIR;
done
#
# EOF
