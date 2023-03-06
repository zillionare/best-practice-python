echo "converting $1..."

if [ -z "$1" ]; then
    echo "请提供要转换的文件名，包含从当前目录开始的路径。"
    exit
fi 

cur=`pwd`

from_dir="$(dirname $1)"

file="$(basename $1)"
stem="${file%.*}"

to="/apps/best-practice-python/word_document/$stem.docx"
echo "from=$file, to=$to, in $from_dir"

python preprocessors/word.py preprocess "$from_dir/$file"
cd $from_dir
pandoc --lua-filter /apps/best-practice-python/preprocessors/admonition.lua -o $to -f markdown -t docx /tmp/$file  --reference-doc=$cur/template.docx

cd $cur
