#!/bin/bash
num=$(grep ^ -n $1| tail -n 1 | cut -d : -f1)
index=1
echo "[" > $2
cat $1 | while read line; do
    echo "{" >> $2
    ss=(${line})

        echo "\"${ss[0]}\": \"${ss[1]}\"," >> $2
        echo "\"name\": \"${ss[3]}\"," >> $2
        echo "\"type\": \"${ss[2]}\"," >> $2
        if [ "${#ss[@]}" -gt 4 ]
    then
        echo "\"options\": {" >> $2
        str1="\"value\":["
        str2="\"label\":["
        for ((i=4;i<${#ss[*]};i+=2))
        do
            if [ $i == 4 ]
            then
                c1=""
            else
                c1=","
            fi
            str1=$str1"$c1\"${ss[$i]}\""
            str2=$str2"$c1\"${ss[$i + 1]}\""
            if [ "${#ss[*]}" == "$[$i+1]" ]
            then
              str1=$str1","
              str2=$str2","
            fi
        done
        str1=$str1"],"
        str2=$str2"]"
        echo $str1 >> $2
        echo $str2 >> $2
        echo "}" >> $2
    else
        echo "\"options\": {}" >> $2
    fi
    if [ $index -eq $num ]
    then
        echo "}" >> $2
    else
        echo "}," >> $2
    fi
    index=$[$index+1]
done
echo "]" >> $2
