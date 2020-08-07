#!/bin/bash

#Author: Ariwori  i@wqlin.com
DST_HOME="${HOME}/DST"
dst_conf_dirname="DoNotStarveTogether"
dst_conf_basedir="${DST_HOME}/Klei"
dst_base_dir="${dst_conf_basedir}/${dst_conf_dirname}"
dst_server_dir="${DST_HOME}/DSTServer"
dst_bin_cmd="./dontstarve_dedicated_server_nullrenderer"
data_dir="${DST_HOME}/dstscript"
dst_token_file="${data_dir}/clustertoken.txt"
server_conf_file="${data_dir}/server.conf"
dst_cluster_file="${data_dir}/clusterdata.txt"
log_arr_str="${data_dir}/logarr.txt"
ays_log_file="${data_dir}/ays_log_file.txt"
log_save_dir="${dst_conf_basedir}/LogBackup"
mod_cfg_dir="${data_dir}/modconfigure"
cluster_backup_dir="${dst_conf_basedir}/ClusterBackup"
my_api_link="https://wqlin.com/tools/dst.php"
feed_back_link="https://wqlin.com/archives/157.html"
script_url="https://wqlin.com/usr/uploads/myfiles/shell/dstserver.sh"
# 屏幕输出
Green_font_prefix="\033[32m"
Red_font_prefix="\033[31m"
Yellow_font_prefix="\033[33m"
Font_color_suffix="\033[0m"
Info="${Green_font_prefix}[信息]${Font_color_suffix}"
Error="${Red_font_prefix}[错误]${Font_color_suffix}"
Tip="${Yellow_font_prefix}[提示]${Font_color_suffix}"
info(){
  echo -e "${Info}" "$1"
}
tip(){
  echo -e "${Tip}" "$1"
}
error(){
  echo -e "${Error}" "$1"
}
# Main menu
Menu(){
  while (true)
  do
    Get_game_beta_str
    echo -e "\e[33m============欢迎使用饥荒联机版独立服务器脚本[Linux-Steam]============\e[0m"
    echo -e "\e[33m作者：Ariwori(i@wqlin.com) 更新地址==>${feed_back_link}\e[0m"
    echo -e "\e[33m本脚本一切权利归作者所有。未经许可禁止使用本脚本进行任何的商业活动！\e[0m"
    echo -e "\e[31m游戏服务端安装目录：${dst_server_dir} [$gamebeta_str(Version: $(cat "${dst_server_dir}/version.txt"))]\e[0m"
    echo -e "\e[92m[ 1]启动服务器           [ 2]关闭服务器           [ 3]重启服务器\e[0m"
    echo -e "\e[92m[ 4]修改房间设置         [ 5]MOD管理及配置        [ 6]特殊名单管理\e[0m"
    echo -e "\e[92m[ 7]游戏服务端控制台     [ 8]附加功能设置         [ 9]重置脚本数据\e[0m"
    echo -e "\e[92m[10]存档管理             [11]更新游戏服务端       [12]更新MOD\e[0m"
    echo -e "\e[92m[13]当前玩家记录         [14]查看附加进程         [15]测试版本切换\e[0m"
    # echo -e "\e[92m[16]更新脚本\e[0m"
    echo -e "\e[92m[16]更新脚本             [17]删除Steam缓存(游戏更新失败修复使用)\e[0m"
    # echo -e "\e[92m[18]设置/修改Steam账号\e[31m(选项[17]无效可尝试, 改完先执行一次[17])\e[0m"
    Simple_server_status
    echo -e "\e[33m====================================================================\e[0m"
    echo -e "\e[92m[退出或中断操作请直接按Ctrl+C]请输入命令代号：\e[0m\c"
    read -r cmd
    case "${cmd}" in
      1)
      Start_server
      ;;
      2)
      Close_server
      Exit_auto_update
      ;;
      3)
      Reboot_server
      ;;
      4)
      Change_cluster
      ;;
      5)
      MOD_manager
      ;;
      6)
      List_manager
      ;;
      7)
      Server_console
      ;;
      8)
      Extend_function_setting
      ;;
      9)
      Reset_data
      ;;
      10)
      Cluster_manager
      ;;
      11)
      Update_DST
      ;;
      12)
      Update_MOD
      ;;
      13)
      Show_players
      ;;
      14)
      Get_in_EFS
      ;;
      15)
      Changeversion
      ;;
      16)
      Update_script
      ;;
      17)
      Remove_steam_cache
      ;;
      # 18)
      # Set_steam_user
      # ;;
      *)
      error "输入有误！！！"
      ;;
    esac
  done
}
Set_steam_user(){
  if [ ! -f ${data_dir}/userinfo.txt ]
  then
    touch ${data_dir}/userinfo.txt
  fi
  rm ${data_dir}/userinfo.txt
  touch ${data_dir}/userinfo.txt

  echo -e "\e[92m请输入新的用户名，不改直接回车：\e[0m\c"
  read -r newuser
  if [ -z $newuser ]
  then
    echo "user=anonymous" > ${data_dir}/userinfo.txt
  else
    echo "user=${newuser}" > ${data_dir}/userinfo.txt
  fi

  echo -e "\e[92m请输入新的密码，不改直接回车：\e[0m\c"
  read -r newpasswd
  if [ -z $newpasswd ]
  then
    echo "password=" >> ${data_dir}/userinfo.txt
  else
    echo "password=${newpasswd}" >> ${data_dir}/userinfo.txt
  fi
  tip "Steam用户信息修改完毕！更新游戏过程中可能需要输入手机令牌或邮箱验证码！"
}
Remove_steam_cache(){
  rm -rf ${HOME}/Steam >/dev/null 2>&1
  info "安装缓存清理完毕！"
}
Diff_file(){
  cmp -s $1 $2
  if [ $? -eq 1 ]
  then
    return 0
  else
    return 1
  fi
}
Update_script(){
  info "正在检查脚本是否有更新 ..."
  wget ${script_url} -O /tmp/dstserver.sh -o /tmp/dstupdate.log
  if grep "‘/tmp/dstserver.sh’ saved" /tmp/dstupdate.log > /dev/null 2>&1
  then
    if Diff_file /tmp/dstserver.sh ${HOME}/dstserver.sh
    then
      mv /tmp/dstserver.sh ${HOME}/dstserver.sh
      chmod +x ${HOME}/dstserver.sh
      tip "脚本已更新并退出，重新运行以使更新生效，如更新后异常请查看脚本更新页面说明！"
      exit
    else
      info "脚本没有更新可用！"
    fi
  else
    error "无法连接更新服务，请重试，多次不行请反馈或不更新！"
  fi
}
Get_game_beta(){
  [ -f "${server_conf_file}" ] && gamebeta=$(grep "^gamebeta" "${server_conf_file}" | cut -d "=" -f2)
}
Get_game_beta_str(){
  public_str="正式版"
  returnofthembeta_str="旧神归来"
  Get_game_beta
  if [[ $gamebeta == "" ]]
  then
    gamebeta="public"
  fi
  gamebeta_str=`eval echo '$'"$gamebeta"_str`
  if [[ $gamebeta_str == "" ]]
  then
    gamebeta_str="测试版"
  fi
}
Changeversion(){
  Get_game_beta_str
  info "当前版本[$gamebeta_str($gamebeta)]，切换为版本：1.正式版 2.旧神归来 3.自定义 0.退出"
  read beta
  case $beta in
    1)
    new_gamebeta="public"
    ;;
    2)
    new_gamebeta="returnofthembeta"
    ;;
    3)
    info "请输入测试版本代码：\c"
    read custom_beta
    new_gamebeta=$custom_beta
    ;;
    4)
    tip "已退出版本切换！"
    ;;
  esac
  if [[ $new_gamebeta != "" ]]
  then
    exchangesetting gamebeta $new_gamebeta
    new_gamebeta_str=`eval echo '$'"$new_gamebeta"_str`
    if [[ $new_gamebeta_str == "" ]]
    then
      $new_gamebeta_str="测试版"
    fi
    info "已切换游戏版本为[$new_gamebeta_str($new_gamebeta)]，请更新游戏以生效！"
  fi
}
Get_in_EFS(){
  if tmux has-session -t Auto_update > /dev/null 2>&1
  then
    tmux attach -t Auto_update
  else
    tip "附加功能进程未开启或已异常退出！"
  fi
}
Change_cluster(){
  Get_current_cluster
  if [ -d "$dst_base_dir/${cluster}" ]
  then
    Set_cluster
  else
    error "当前存档【${cluster}】已被删除或已损坏！"
  fi
}
Server_console(){
  Get_single_shard
  if tmux has-session -t DST_"${shard}" > /dev/null 2>&1
  then
    info "即将跳转${shard}世界后台。。。退出请按Ctrl + B松开再按D，否则服务器将停止运行！！！"
    sleep 3
    tmux attach-session -t DST_"${shard}"
  else
    tip "${shard}世界未开启或已异常退出！！！"
  fi
}
Get_shard_array(){
  Get_current_cluster
  [[ $cluster != "无" ]] && [ -d "$dst_base_dir/${cluster}" ] && shardarray=$(ls -l "$dst_base_dir/${cluster}" | grep ^d | awk '{print $9}')
}
Get_single_shard(){
  Get_current_cluster
  Get_shard_array
  for shard in ${shardarray}
  do
    shardm=$shard
    if [ -f "${dst_base_dir}/${cluster}/${shardm}/server.ini" ]
    then
      if [ $(grep 'is_master = true' -c "${dst_base_dir}/${cluster}/${shardm}/server.ini") -gt 0 ]
      then
        shardm=$shard
        break
      fi
    else
      error "存档【${cluster}】世界【${shardm}】配置文件server.ini缺失，存档损坏！"
      exit
    fi
  done
  [ -z "$shardm" ] && shard=$shardm
}
Get_current_cluster(){
  [ -f "${server_conf_file}" ] && cluster=$(grep "^cluster" "${server_conf_file}" | cut -d "=" -f2)
  [ -z $cluster ] && cluster="无"
}
Get_server_status(){
  [ -f "${server_conf_file}" ] && serveropen=$(grep "serveropen" "${server_conf_file}" | cut -d "=" -f2)
}
MOD_manager(){
  Get_current_cluster
  if [ -d "${dst_base_dir}/${cluster}" ]
  then
    if [ $( ls -l "${dst_base_dir}/${cluster}" | grep -c ^d) -gt 0 ]
    then
      Default_mod
      while (true)
      do
        echo -e "\e[92m【存档：${cluster}】 你要\n1.添加mod       2.删除mod      3.修改MOD配置 \n4.重置MOD配置   5.安装MOD合集  6.返回主菜单\n：\e[0m\c"
        read mc
        case "${mc}" in
          1)
          Listallmod
          Addmod;;
          2)
          Listusedmod
          Delmod;;
          3)
          Mod_Cfg;;
          4)
          Clear_mod_cfg
          ;;
          5)
          Install_mod_collection
          ;;
          6)
          tip "MOD的更改必须重启服务器后才会生效！！！"
          break
          ;;
          *)
          error "输入有误！！！"
          ;;
        esac
      done
      Removelastcomma
    else
      error "当前存档【${cluster}】已被删除或已损坏！"
    fi
    else
    error "当前存档【${cluster}】已被删除或已损坏！"
    fi
}
Install_mod_collection(){
  [ -f "$data_dir/modcollectionlist.txt" ] && rm -rf "$data_dir/modcollectionlist.txt"
  touch "$data_dir/modcollectionlist.txt"
  echo -e "\e[92m[输入结束请输入数字 0]请输入你的MOD合集ID:\e[0m\c"
  while (true)
  do
    read clid
    if [ $clid -eq 0 ]
    then
      info "合集添加完毕！即将安装 ..."
      break
    else
      echo "ServerModCollectionSetup(\"$clid\")" >> "$data_dir/modcollectionlist.txt"
      info "该MOD合集($clid)已添加到待安装列表。"
    fi
  done
  if [ -s "$data_dir/modcollectionlist.txt" ]
  then
    info "正在安装新添加的MOD(合集)，请稍候 。。。"
    if [ ! -d "${dst_base_dir}/downloadmod/Master" ]
    then
      mkdir -p "${dst_base_dir}/downloadmod/Master"
    fi
    if tmux has-session -t DST_MODUPDATE > /dev/null 2>&1
    then
      tmux kill-session -t DST_MODUPDATE
    fi
    cp "$data_dir/modcollectionlist.txt" "${dst_server_dir}/mods/dedicated_server_mods_setup.lua"
    cd "${dst_server_dir}/bin" || exit 1
    tmux new-session -s DST_MODUPDATE -d "${dst_bin_cmd} -persistent_storage_root ${dst_conf_basedir} -cluster downloadmod -shard Master"
    sleep 3
    while (true)
    do
      if tmux has-session -t DST_MODUPDATE > /dev/null 2>&1
      then
        if [ $(grep "Your Server Will Not Start" -c "${dst_base_dir}/downloadmod/Master/server_log.txt") -gt 0 ]
        then
          info "安装进程已执行完毕，请到添加MOD中查看是否安装成功！"
          tmux kill-session -t DST_MODUPDATE
          break
        fi
      fi
    done
  else
    tip "没有新的MOD合集需要安装！"
  fi
}
Clear_mod_cfg(){
  [ -d "$mod_cfg_dir" ] && rm -rf $mod_cfg_dir
  info "所有MOD配置均已重置！"
}
Mod_Cfg(){
  while (true)
  do
    clear
    Get_current_cluster
    echo -e "\e[92m【存档：${cluster}】已启用的MOD配置修改===============\e[0m"
    Listusedmod
    info "请从以上列表选择你要配置的MOD${Red_font_prefix}[编号]${Font_color_suffix},完毕请输数字 0 ！"
    read modid
    if [[ "${modid}" == "0" ]]
    then
      info "MOD配置完毕！"
      break
    else
      Truemodid #moddir
      Show_mod_cfg
      Write_mod_cfg
    fi
  done
}
# 传入moddir
Show_mod_cfg(){
  if [ -f "${mod_cfg_dir}/${moddir}.cfg" ]
  then
    Get_installed_mod_version
    n_ver=$result
    Get_data_from_file "${mod_cfg_dir}/${moddir}.cfg" mod-version
    c_ver=$result
    if [[ "$n_ver" != "$c_ver" ]]
    then
      update_mod_cfg
    fi
  else
    update_mod_cfg
  fi
  Get_data_from_file "${mod_cfg_dir}/${moddir}.cfg" "mod-configureable"
  c_able=$result
  c_line=$(grep "^" -n "${mod_cfg_dir}/${moddir}.cfg"| tail -n 1 | cut -d : -f1)
  if [[ "$c_able" == "true" && "$c_line" -gt 3 ]]
  then
    Get_data_from_file "${mod_cfg_dir}/${moddir}.cfg" "mod-version"
    c_ver=$result
    Get_data_from_file "${mod_cfg_dir}/${moddir}.cfg" "mod-name"
    c_name=$(echo $result | sed 's/#/ /g')
    while (true)
    do
      clear
      echo -e "\e[92m【修改MOD：$c_name配置】[$c_ver]\e[0m"
      index=1
      cat "${mod_cfg_dir}/${moddir}.cfg" | grep -v "mod-configureable" | grep -v "mod-version" | grep -v "mod-name" | while read line
      do
        ss=(${line})
        if [ "${ss[2]}" == "table" ]
        then
          value=${ss[1]}
        else
          for ((i=5;i<${#ss[*]};i=$i+3))
          do
            if [ "${ss[$i]}" == "${ss[1]}" ]
            then
              value=${ss[$i+1]}
            fi
          done
        fi
        if [[ "$value" == "不明项勿修改" ]]
        then
          value=${ss[1]}
        fi
        value=$(echo "$value" | sed 's/#/ /g')
        label=$(echo "${ss[3]}" | sed 's/#/ /g')
        hover=$(echo "${ss[4]}" | sed 's/#/ /g')
        if [[ "$label" == "" || "$label" == "nolabel" ]]
        then
          label=$(echo "${ss[0]}" | sed 's/#/ /g')
          hover="${Red_font_prefix}该项作用不明，请勿轻易修改否则可能出错。详情请查看modinfo.lua文件。${Font_color_suffix}"
        fi
        if [ "${index}" -lt 10 ]
        then
          echo -e "\e[33m[ ${index}] $label：${Red_font_prefix}${value}${Font_color_suffix}\n     简介==>$hover\e[0m"
        else
          echo -e "\e[33m[${index}] $label：${Red_font_prefix}${value}${Font_color_suffix}\n     简介==>$hover\e[0m"
        fi
        index=$(($index + 1))
      done
      echo -e "\e[92m===============================================\e[0m"
      unset cmd
      while (true)
      do
        if [[ "${cmd}" == "" ]]
        then
          echo -e "\e[92m请选择你要更改的选项(修改完毕输入数字 0 确认修改并退出)：\e[0m\c"
          read cmd
        else
          break
        fi
      done
      case "${cmd}" in
        0)
        info "更改已保存！"
        break
        ;;
        *)
        cmd=$(($cmd + 3))
        changelist=($(sed -n "${cmd}p" "${mod_cfg_dir}/${moddir}.cfg"))
        label=$(echo "${changelist[3]}" | sed 's/#/ /g')
        if [[ "$label" == "" || "$label" == "nolabel" ]]
        then
          label=$(echo "${changelist[0]}" | sed 's/#/ /g')
        fi
        if [ "${changelist[2]}" = "table" ]
        then
          tips "${Red_font_prefix}此项为表数据，请直接修改modinfo.lua文件${Font_color_suffix}"
        else
          echo -e "\e[92m请选择$label： \e[0m"
          index=1
          for ((i=5;i<${#changelist[*]};i=$i+3))
          do
            description=$(echo "${changelist[$[$i + 1]]}" | sed 's/#/ /g')
            hover=$(echo "${changelist[$[$i + 2]]}" | sed 's/#/ /g')
            printf "%-30s" "${index}.$description"
            echo -e "\e[92m简介==>$hover\e[0m"
            index=$((${index} + 1))
          done
          echo -e "\e[92m: \e[0m\c"
          read changelistindex
          listnum=$[${changelistindex} - 1]*3
          changelist[1]=${changelist[$[$listnum + 5]]}
        fi
        changestr="${changelist[@]}"
        sed -i "${cmd}c ${changestr}" "${mod_cfg_dir}/${moddir}.cfg"
        ;;
      esac
    done
    fi
}
Write_mod_cfg(){
    Delmodfromshard > /dev/null 2>&1
    rm "${data_dir}/modconfwrite.lua" > /dev/null 2>&1
    touch "${data_dir}/modconfwrite.lua"
    if [ -f "${mod_cfg_dir}/${moddir}.cfg" ]
    then
    c_line=$(grep "^" -n "${mod_cfg_dir}/${moddir}.cfg"| tail -n 1 | cut -d : -f1)
    if [[ $c_line -le 3 ]]
    then
      echo "  [\"$moddir\"]={ [\"enabled\"]=true }," >> "${data_dir}/modconfwrite.lua"
    else
      echo "  [\"$moddir\"]={" >> "${data_dir}/modconfwrite.lua"
      echo "    configuration_options={" >> "${data_dir}/modconfwrite.lua"
      # cindex=4
      cat "${mod_cfg_dir}/${moddir}.cfg"| grep -v "mod-configureable" | grep -v "mod-version" | grep -v "mod-name" | while read lc
      do
        lcstr=($lc)
        cfgname=$(echo "${lcstr[0]}" | sed 's/#/ /g')
        if [[ "${lcstr[2]}" != "table" ]]
        then
          if [[ "${lcstr[2]}" == "number" ]]
          then
            echo -e "      [\"$cfgname\"]=${lcstr[1]}," >> "${data_dir}/modconfwrite.lua"
          elif [[ "${lcstr[2]}" == "string" ]]
          then
            echo -e "      [\"$cfgname\"]=\"${lcstr[1]}\"," >> "${data_dir}/modconfwrite.lua"
          elif [[ "${lcstr[2]}" == "boolean" ]]
          then
            echo -e "      [\"$cfgname\"]=${lcstr[1]}," >> "${data_dir}/modconfwrite.lua"
          fi
        fi
      done
      echo "    }," >> "${data_dir}/modconfwrite.lua"
      echo "    [\"enabled\"]=true" >> "${data_dir}/modconfwrite.lua"
      echo "  }," >> "${data_dir}/modconfwrite.lua"
    fi
    else
    echo "  [\"$moddir\"]={ [\"enabled\"]=true }," >> "${data_dir}/modconfwrite.lua"
    fi
    Addmodtoshard > /dev/null 2>&1
}
Get_data_from_file(){
    if [ -f "$1" ]
    then
    result=$(grep "^$2" "$1" |head -n 1 | cut -d " " -f3)
    fi
}
Get_installed_mod_version(){
  if [ -f "${dst_server_dir}/mods/${moddir}/modinfo.lua" ]
  then
    echo "fuc=\"getver\"" > "${data_dir}/modinfo.lua"
    cat "${dst_server_dir}/mods/${moddir}/modinfo.lua" >> "${data_dir}/modinfo.lua"
    cd "${data_dir}"
    result=$(lua modconf.lua)
    cd ${DST_HOME}
  else
    result="uninstalled"
  fi
}
update_mod_cfg(){
    if [[ -f "${dst_server_dir}/mods/${moddir}/modinfo.lua" ]]
    then
    cat > "${data_dir}/modinfo.lua" <<-EOF
fuc = "createmodcfg"
modid = "${moddir}"
EOF
    cat "${dst_server_dir}/mods/${moddir}/modinfo.lua" >> "${data_dir}/modinfo.lua"
    if [[ -f "${dst_server_dir}/mods/${moddir}/modinfo_chs.lua" ]]
    then
      cat "${dst_server_dir}/mods/${moddir}/modinfo_chs.lua" >> "${data_dir}/modinfo.lua"
    fi
    cd "${data_dir}"
    lua modconf.lua >/dev/null 2>&1
    cd "${DST_HOME}"
    else
    tip "请先安装并启用MOD！"
    break
    fi
}
MOD_conf(){
    if [[ "${fuc}" == "createmodcfg" ]]
    then
    if [[ -f "${dst_server_dir}/mods/${moddir}/modinfo.lua" ]]
    then
      cat "${dst_server_dir}/mods/${moddir}/modinfo.lua" >> "${data_dir}/modinfo.lua"
    else
      needdownloadid=$(echo "${moddir}" | cut -d "-" -f2)
      echo "ServerModSetup(\"$needdownloadid\")" > "${dst_server_dir}/mods/dedicated_server_mods_setup.lua"
      # 当输入多个MODID时，在第一次下载时全部添加下载
      for exmodid in ${inputarray[@]}
      do
        if [ $exmodid -gt 100000 ]
        then
          echo "ServerModSetup(\"$exmodid\")" >> "${dst_server_dir}/mods/dedicated_server_mods_setup.lua"
        fi
      done
      Download_MOD
    fi
    if [[ -f "${dst_server_dir}/mods/${moddir}/modinfo.lua" ]]
    then
      if [ ! -f "${mod_cfg_dir}/${moddir}.cfg" ]
      then
        update_mod_cfg
      fi
    else
      error "MOD安装失败，无法继续请上传MOD或重试！"
      exit 0
    fi
    else
    cat > "${data_dir}/modinfo.lua" <<-EOF
fuc = "${fuc}"
modid = "${moddir}"
used = "${used}"
EOF
    if [[ -f "${dst_server_dir}/mods/${moddir}/modinfo.lua" ]]
    then
      cat "${dst_server_dir}/mods/${moddir}/modinfo.lua" >> "${data_dir}/modinfo.lua"
    else
      echo "name = \"UNKNOWN\"" >> "${data_dir}/modinfo.lua"
    fi
    cd ${data_dir}
    lua modconf.lua >/dev/null 2>&1
    cd ${DST_HOME}
    fi
}
Listallmod(){
  if [ ! -f "${data_dir}/mods_setup.lua" ]
  then
    touch "${data_dir}/mods_setup.lua"
  fi
  rm -f "${data_dir}/modconflist.lua"
  touch "${data_dir}/modconflist.lua"
  Get_single_shard
  for moddir in $(ls -F "${dst_server_dir}/mods" | grep "/$" | cut -d '/' -f1)
  do
    if [ $(grep "${moddir}" -c "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua") -gt 0 ]
    then
      used="true"
    else
      used="false"
    fi
    if [[ "${moddir}" != "" ]]
    then
      fuc="list"
      MOD_conf
    fi
  done
  if [ ! -s  "${data_dir}/modconflist.lua" ]
  then
    tip "没有安装任何MOD，请先安装MOD！！！"
  else
    grep -n "^" "${data_dir}/modconflist.lua"
  fi
}
Listusedmod(){
  rm -f "${data_dir}/modconflist.lua"
  touch "${data_dir}/modconflist.lua"
  Get_single_shard
  for moddir in $(grep "^  \[" "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua" | cut -d '"' -f2)
  do
    used="false"
    if [[ "${moddir}" != "" ]]
    then
      fuc="list"
      used="true"
      MOD_conf
    fi
  done
  if [ ! -s  "${data_dir}/modconflist.lua" ]
  then
    tip "没有启用任何MOD，请先启用MOD！！！"
  else
    grep -n "^" "${data_dir}/modconflist.lua"
  fi
}
Addmod(){
    info "请从以上列表选择你要启用的MOD${Red_font_prefix}[编号]${Font_color_suffix}，不存在的直接输入MODID"
    tip "大小超过10M的MOD如果无法在服务器添加下载，请手动上传到服务器再启用！！！"
    info "添加完毕要退出请输入数字 0 ！[可输入多个，如 \"1 2 4-6 7927397293\"]"
    while (true)
    do
    read modid
    if [[ "${modid}" == "0" ]]
    then
      info "添加完毕 ！"
      break
    fi
    if [[ "${modid}" == "" ]]
    then
      error "输入不可为空值！！！"
    else
      Getinputlist "$modid"
      for modid in ${inputarray[@]}
      do
        Addmodfunc
      done
    fi
    done
    clear
    info "默认参数配置已写入配置文件，可手动修改，也可通过脚本修改："
    info "${dst_base_dir}/${cluster}/***/modoverrides.lua"
}
Addmodtoshard(){
    Get_shard_array
    for shard in ${shardarray}
    do
    if [ -f "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua" ]
    then
      if [ $(grep "${moddir}" -c "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua") -gt 0 ]
      then
        info "${shard}世界该Mod(${moddir})已添加"
      else
        sed -i '1d' "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua"
        cat "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua" > "${data_dir}/modconftemp.txt"
        echo "return {" > "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua"
        cat "${data_dir}/modconfwrite.lua" >> "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua"
        cat "${data_dir}/modconftemp.txt" >> "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua"
        info "${shard}世界Mod(${moddir})添加完成"
      fi
    else
      tip "${shard} MOD配置文件未由脚本初始化，无法操作！如你已自行配置请忽略本提示！"
    fi
    done
}
Truemodid(){
    if [ ${modid} -lt 10000 ]
    then
    moddir=$(sed -n ${modid}p "${data_dir}/modconflist.lua" | cut -d ':' -f3)
    else
    moddir="workshop-${modid}"
    fi
}
Addmodfunc(){
    Truemodid
    fuc="createmodcfg"
    MOD_conf
    Write_mod_cfg
    Addmodtoshard
    Removelastcomma
}
Delmodfromshard(){
    Get_shard_array
    for shard in ${shardarray}
    do
    if [ -f "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua" ]
    then
      if [ $(grep "${moddir}" -c "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua") -gt 0 ]
      then
        grep -n "^  \[" "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua" > "${data_dir}/modidlist.txt"
        lastmodlinenum=$(cat "${data_dir}/modidlist.txt" | tail -n 1 | cut -d ":" -f1)
        up=$(grep "${moddir}" "${data_dir}/modidlist.txt" | cut -d ":" -f1)
        if [ "${lastmodlinenum}" -eq "${up}" ]
        then
          down=$(grep "^" -n "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua" | tail -n 1 | cut -d ":" -f1)
        else
          down=$(grep -A 1 "${moddir}" "${data_dir}/modidlist.txt" | tail -1 |cut -d ":" -f1)
        fi
        upnum=${up}
        downnum=$((${down} - 1))
        sed -i "${upnum},${downnum}d" "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua"
        info "${shard}世界该Mod(${moddir})已停用！"
      else
        info "${shard}世界该Mod(${moddir})未启用！"
      fi
    else
      tip "${shard} MOD配置文件未由脚本初始化，无法操作！如你已自行配置请忽略本提示！"
    fi
    done
}
# 保证最后一个MOD配置结尾不含逗号
Removelastcomma(){
    for shard in ${shardarray}
    do
    if [ -f "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua" ]
    then
      checklinenum=$(grep "^" -n "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua" | tail -n 2 | head -n 1 | cut -d ":" -f1)
      sed -i "${checklinenum}s/,//g" "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua"
    fi
    done
}
Delmod(){
    info "请从以上列表选择你要停用的MOD${Red_font_prefix}[编号]${Font_color_suffix}[可多选，如输入\"1 2 4-6\"],完毕请输数字 0 ！"
    while (true)
    do
    read modid
    if [[ "${modid}" == "0" ]]
    then
      info "MOD删除完毕！"
      break
    else
      Getinputlist "$modid"
      for modid in ${inputarray[@]}
      do
        Truemodid
        Delmodfromshard
      done
    fi
    done
}
List_manager(){
    tip "添加的名单设置在重启后生效，且在每一个存档都会生效！"
    while (true)
    do
    echo -e "\e[92m你要设置：1.管理员  2.黑名单  3.白名单 4.返回主菜单? \e[0m\c"
    read list
    case "${list}" in
      1)
      listfile="alist.txt"
      listname="管理员"
      ;;
      2)
      listfile="blist.txt"
      listname="黑名单"
      ;;
      3)
      listfile="wlist.txt"
      listname="白名单"
      ;;
      4)
      break
      ;;
      *)
      error "输入有误，请输入数字[1-3]"
      ;;
    esac
    while (true)
    do
      echo -e "\e[92m你要：1.添加${listname} 2.移除${listname} 3.返回上一级菜单? \e[0m\c"
      read addordel
      case "${addordel}" in
        1)
        Addlist
        ;;
        2)
        Dellist
        ;;
        3)
        break
        ;;
        *)
        error "输入有误！"
        ;;
      esac
    done
    done
}
Addlist(){
    echo -e "\e[92m请输入你要添加的KLEIID（KU_XXXXXXX）：(添加完毕请输入数字 0 )\e[0m"
    while (true)
    do
    read kleiid
    if [[ "${kleiid}" == "0" ]]
    then
      info "添加完毕！"
      break
    else
      if [ $(grep "${kleiid}" -c "${data_dir}/${listfile}") -gt 0 ]
      then
        info "名单${kleiid}已经存在！"
      else
        echo "${kleiid}" >> "${data_dir}/${listfile}"
        info "名单${kleiid}已添加！"
      fi
    fi
    done
}
Dellist(){
    while (true)
    do
    echo "=========================================================================="
    grep -n "^" "${data_dir}/${listfile}"
    echo -e "\e[92m请输入你要移除的KLEIID${Red_font_prefix}[编号]${Font_color_suffix}，删除完毕请输入数字 0 \e[0m"
    read kleiid
    if [[ "${kleiid}" == "0" ]]
    then
      info "移除完毕！"
      break
    else
      sed -i "${kleid}d" "${data_dir}/${listfile}"
      info "名单已移除！"
    fi
    done
}
Restore_cluster(){
    #ss="$(ls$cluster_backup_dir/$cur_day/cluster_backup_${cluster}_${cur_time}.tar.gz"
    if [ $(ls $cluster_backup_dir | grep -c ^) -gt 0 ]
    then
    echo -e "\e[92m 请选择日期：\c"
    dindex=1
    for ddate in $(ls $cluster_backup_dir)
    do
      echo -e "$dindex.$ddate   \c"
      dindex=$(($dindex +1))
    done
    echo -e "\e[0m\c"
    read dddate
    ddddate=$(ls $cluster_backup_dir | head -n $dddate | tail -n 1)
    if [ $(ls $cluster_backup_dir/$ddddate | grep -c ^) -gt 0 ]
    then
      ls -rc $cluster_backup_dir/$ddddate | grep -n ^
      echo -e "\e[92m 请选择要恢复的存档：\e[0m\c"
      read clustersnum
      clustersname=$(ls -rc $cluster_backup_dir/$ddddate | head -n $clustersnum | tail -n 1)
      mycluster=$(echo $clustersname | cut -d "_" -f3)
      Get_current_cluster
      Get_server_status
      if [[ "$mycluster" == "$cluster" && "$serveropen" == "true" ]]
      then
        error "存档【$mycluster】正在运行，请关闭后再恢复！！"
      else
        tar -xzPf $cluster_backup_dir/$ddddate/$clustersname
        info "存档【$mycluster】已恢复！"
      fi
    else
      error "日期【$ddddate】没有任何备份！"
    fi
    else
    error "当前没有任何备份！"
    fi
}
Cluster_manager(){
    while (true)
    do
    echo -e "\e[92m你要：1.删除存档  2.恢复存档   3.返回主菜单? \e[0m\c"
    read clusterst
    case $clusterst in
      1)
      Del_cluster
      ;;
      2)
      Restore_cluster
      ;;
      3)
      break
      ;;
      *)
      error "输入有误！！！"
      ;;
    esac
    done
}
Del_cluster(){
    cluster_str="删除"
    inputtips='[可多选，如输入"1 2 4-6"]'
    Choose_exit_cluster
    Getinputlist "$listnum"
    for listnum in ${inputarray[@]}
    do
    unset mycluster
    if [ $listnum -ne 0 ]
    then
      mycluster=$(cat "/tmp/dirlist.txt" | head -n "${listnum}" | tail -n 1)
    fi
    if [ ! -z $mycluster ]
    then
      Get_current_cluster
      Get_server_status
      if [[ "$mycluster" == "$cluster" && "$serveropen" == "true" ]]
      then
        error "存档【$mycluster】正在运行，请关闭后再删除！！"
      else
        rm -rf "${dst_base_dir}/${mycluster}" && info "存档【${mycluster}】已删除！"
      fi
    fi
    done
}
Auto_update(){
    Get_single_shard
    if tmux has-session -t DST_"${shard}" > /dev/null 2>&1
    then
    tmux kill-session -t Auto_update > /dev/null 2>&1
    sleep 1
    tmux new-session -s Auto_update -d "bash ${HOME}/dstserver.sh au"
    info "附加功能已开启！"
    else
    tip "${shard}世界未开启或已异常退出！无法启用附加功能！"
    fi
}
Show_players(){
    Get_single_shard
    if tmux has-session -t DST_"${shard}" > /dev/null 2>&1
    then
    if tmux has-session -t Show_players > /dev/null 2>&1
    then
      info "即将跳转。。。退出请按Ctrl + B松开再按D！"
      tmux attach-session -t Show_players
      sleep 1
    else
      tmux new-session -s Show_players -d "bash ${HOME}/dstserver.sh sp"
      tmux split-window -t Show_players
      tmux send-keys -t Show_players:0 "bash ${HOME}/dstserver.sh sa" C-m
      info "进程已开启。。。请再次执行命令进入!"
    fi
    else
    tip "${shard}世界未开启或已异常退出！无法启用玩家日志后台！"
    fi
}
Update_DST(){
    info "这将关闭正在运行的服务器，是否继续？ 1.是 2.否："
    read cp
    if [ $cp -eq 1 ]
    then
    Get_server_status
    cur_serveropen=${serveropen}
    Reboot_announce
    Close_server
    Install_Game
    else
    tip "操作已中断！"
    fi
}
###################################################################
Reboot_server(){
    info "服务器重启中。。。请稍候。。。"
    Reboot_announce
    Close_server
    Run_server
}
exchangesetting(){
    if [ ! -f "${server_conf_file}" ]
    then
    touch "${server_conf_file}"
    fi
    if [ $(grep "^$1=" -c "${server_conf_file}") -gt 0 ]
    then
    linen=$(grep "^$1=" -n "${server_conf_file}" | cut -d ":" -f1)
    sed -i ${linen}d "${server_conf_file}"
    echo "$1=$2" >> "${server_conf_file}"
    else
    echo "$1=$2" >> "${server_conf_file}"
    fi
}
getsetting(){
    if [ ! -f "${server_conf_file}" ]
    then
    touch "${server_conf_file}"
    fi
    unset result
    if [ $(grep $1 -c "${server_conf_file}") -gt 0 ]
    then
    result=$(grep ^$1 "${server_conf_file}" | head -n 1 | cut -d "=" -f2)
    fi
}
Run_server(){
  Get_current_cluster
  if [ -d "$dst_base_dir/${cluster}" ]
  then
    Get_shard_array
    exchangesetting serveropen true
    Default_mod
    Set_list
    Start_shard
    info "服务器开启中。。。请稍候。。。"
    sleep 5
    Start_check
    Auto_update
  else
    error "存档【${cluster}】已被删除或损坏！服务器无法开启！"
  fi
}
Reboot_announce(){
    Get_shard_array
    for shard in ${shardarray}
    do
    if tmux has-session -t DST_"${shard}" > /dev/null 2>&1
    then
      tmux send-keys -t DST_"${shard}" "c_announce(\"${shard}世界服务器因改动或更新需要重启，预计耗时三分钟，给你带来的不便还请谅解！\")" C-m
    fi
    sleep 5
    done
}
Start_server(){
    info "本操作将会关闭已开启的服务器 ..."
    Close_server
    Exit_auto_update
    echo -e "\e[92m是否新建存档: [y|n] (默认: y): \e[0m\c"
    read yn
    [[ -z "${yn}" ]] && yn="y"
    unset new_cluster
    if [[ "${yn}" == [Yy] ]]
    then
      echo -e "\e[92m请输入新建存档名称：（不要包含中文、符号和空格）\e[0m"
      read cluster
      if [ -d "${dst_base_dir}/${cluster}" ]
      then
        tip "${cluster}存档已存在！是否删除已有存档：1.是  2.否？ "
        read ifdel
        if [[ "$ifdel" -eq 1 ]]
        then
          rm -rf "${dst_base_dir}/${cluster}"
        else
          rm -rf "${dst_base_dir}/${cluster}/cluster.ini"
        fi
      fi
      mkdir -p "${dst_base_dir}/${cluster}"
      Set_cluster
      Set_token
      new_cluster="true"
    else
      cluster_str="开启"
      Choose_exit_cluster
      unset cluster
      if [ $listnum -ne 0 ]
      then
        cluster=$(cat "/tmp/dirlist.txt" | head -n "${listnum}" | tail -n 1)
      fi
      [ -z $cluster ] && error "遇到错误中断！" && exit 0
    fi
    exchangesetting "cluster" "${cluster}"
    if [[ "${new_cluster}" == "true" ]]
    then
      Addshard
    fi
    Import_cluster
    Run_server
}
Addshard(){
    while (true)
    do
    echo -e "\e[92m请选择要添加的世界：1.地面世界  2.洞穴世界  3.添加完成选我\n          快捷设置：4.熔炉MOD[Forged forge]房选我  5.熔炉MOD[ReForged]房选我\n                    6.挂机MOD房选我  7.暴食MOD房选我\n\e[0m\c"
    read shardop
    case "${shardop}" in
      1)
      Addforest;;
      2)
      Addcaves;;
      3)
      break;;
      4)
      Forgeworld
      break;;
      5)
      Reforgedworld
      break;;
      6)
      AOGworld
      break;;
      7)
      Gorgeworld
      break;;
      *)
      error "输入有误，请输入[1-5]！！！";;
    esac
    done
}
Shardconfig(){
    tip "只能有一个主世界！！！熔炉MOD房、挂机MOD房和暴食MOD房只能选主世界！！！"
    info "已创建${shardtype}[$sharddir]，这是一个：1. 主世界   2. 附从世界？ "
    read ismaster
    if [ "${ismaster}" -eq 1 ]
    then
    shardmaster="true"
    shardid=1
    else
    shardmaster="false"
    # 非主世界采用随机数，防止冲突
    shardid=$RANDOM
    fi
    cat > "${dst_base_dir}/${cluster}/$sharddir/server.ini"<<-EOF
[NETWORK]
server_port = $((10997 + $idnum))


[SHARD]
is_master = $shardmaster
name = ${shardname}${idnum}
id = $shardid


[ACCOUNT]
encode_user_path = true


[STEAM]
master_server_port = $((27016 + $idnum))
authentication_port = $((8766 + $idnum))
EOF
}
Getidnum(){
    idnum=$(($(ls -l "${dst_base_dir}/${cluster}" | grep ^d | awk '{print $9}' | grep -c ^) + 1))
}
Createsharddir(){
    sharddir="${shardname}${idnum}"
    mkdir -p "${dst_base_dir}/${cluster}/$sharddir"
}
Addcaves(){
    shardtype="洞穴世界"
    shardname="Caves"
    Getidnum
    Createsharddir
    Shardconfig
    Set_world
}
Addforest(){
    shardtype="地面世界"
    shardname="Forest"
    Getidnum
    Createsharddir
    Shardconfig
    Set_world
}
Gorgeworld(){
  shardtype="暴食MOD房"
    shardname="Gorge"
    Wmodid="1918927570"
    Wconfigfile="quagmire.lua"
    Getidnum
    Createsharddir
    Shardconfig
    Set_world
}
Forgeworld(){
    shardtype="熔炉MOD房[Forged Forge]"
    shardname="Forge"
    Wmodid="1531169447"
    Wconfigfile="lavaarena.lua"
    Getidnum
    Createsharddir
    Shardconfig
    Set_world
}
Reforgedworld(){
    shardtype="熔炉MOD房[ReForged]"
    shardname="ReForge"
    Wmodid="1938752683"
    Wconfigfile="lavaarena1.lua"
    Getidnum
    Createsharddir
    Shardconfig
    Set_world
}
AOGworld(){
    shardtype="挂机MOD房"
    shardname="AOG"
    Wmodid="1210706609"
    Wconfigfile="aog.lua"
    Getidnum
    Createsharddir
    Shardconfig
    Set_world
}
# 导入存档
Import_cluster(){
    Default_mod
    if [ ! -f "${dst_base_dir}/${cluster}/cluster_token.txt" ]
    then
    Set_token
    fi
}
Choose_exit_cluster(){
    echo -e "\e[92m已有存档[退出输入数字 0]：\e[0m"
    ls -l "${dst_base_dir}" | awk '/^d/ {print $NF}' | grep -v downloadmod > "/tmp/dirlist.txt"
    index=1
    for dirlist in $(cat "/tmp/dirlist.txt")
    do
    if [ $(ls -l "${dst_base_dir}/${dirlist}" | grep -c ^d) -gt 0 ]
    then
      if [ -f "${dst_base_dir}/${dirlist}/cluster.ini" ]
      then
        cluster_name_str=$(cat "${dst_base_dir}/${dirlist}/cluster.ini" | grep '^cluster_name =' | cut -d " " -f3)
      fi
      if [[ "$cluster_name_str" == "" ]]
      then
        cluster_name_str="不完整或已损坏的存档"
      fi
    else
      cluster_name_str="不完整或已损坏的存档"
    fi
    echo "${index}. ${dirlist}：${cluster_name_str}"
    let index++
    done
    echo -e "\e[92m请输入你要${cluster_str}的存档${Red_font_prefix}[编号]${Font_color_suffix}${inputtips}：\e[0m\c"
    read listnum
}
Close_server(){
    tip "正在关闭已开启的服务器（有的话） ..."
    unset nodone
    Get_shard_array
    for shard in ${shardarray}
    do
    if tmux has-session -t DST_"${shard}" > /dev/null 2>&1
    then
      tmux send-keys -t DST_"${shard}" "c_shutdown(true)" C-m
      exchangesetting serveropen false
      nodone="true"
    else
      info "${shard}世界服务器未开启！"
    fi
    done
    if [[ "$nodone" == "true" ]]
    then
    for shard in ${shardarray}
    do
      while (true)
      do
        if ! tmux has-session -t DST_"${shard}" > /dev/null 2>&1
        then
          info "${shard}世界服务器已关闭！"
          break
        fi
      done
    done
    for shard in ${shardarray}
    do
      tmux kill-session -t DST_"${shard}" > /dev/null 2>&1
    done
    fi
    Exit_show_players
}
Exit_auto_update(){
    if tmux has-session -t Auto_update > /dev/null 2>&1
    then
    tmux kill-session -t Auto_update > /dev/null 2>&1
    fi
    ps -ef | grep 'dstserver.sh au' | grep -v grep | awk '{print $2}' | xargs kill > /dev/null 2>&1
    info "附加功能进程已停止运行 ..."
}
Exit_show_players(){
    if tmux has-session -t Show_players > /dev/null 2>&1
    then
    tmux kill-session -t Show_players > /dev/null 2>&1
    fi
    ps -ef | grep 'dstserver.sh sp' | grep -v grep | awk '{print $2}' | xargs kill > /dev/null 2>&1
    info "玩家记录后台进程已停止运行 ..."
}
Set_cluster(){
    if [ -f "${dst_base_dir}/${cluster}/cluster.ini" ]
    then
    rm -rf "${dst_base_dir}/${cluster}/cluster.ini"
    fi
    while (true)
    do
    clear
    tip "存档设置修改后需要重启服务器方能生效！！！"
    echo -e "\e[92m=============【存档槽：${cluster}】===============\e[0m"
    index=1
    cat "${dst_cluster_file}" | while read line
    do
      ss=(${line})
      if [ "${ss[4]}" != "readonly" ]
      then
        if [ "${ss[4]}" == "choose" ]
        then
          for ((i=5;i<${#ss[*]};i++))
          do
            if [ "${ss[$i]}" == "${ss[1]}" ]
            then
              value=${ss[$i+1]}
            fi
          done
        else
          # 处理替代空格的#号
          value=$(echo "${ss[1]}" | sed 's/#/ /g')
        fi
        if [ ${index} -lt 10 ]
        then
          echo -e "\e[33m[ ${index}] ${ss[2]}：${value}\e[0m"
        else
          echo -e "\e[33m[${index}] ${ss[2]}：${value}\e[0m"
        fi
      fi
      index=$((${index} + 1))
    done
    echo -e "\e[92m===============================================\e[0m"
    echo -e "\e[31m要开熔炉或暴食MOD房的要先在这里修改游戏模式为对应的游戏模式！！！\e[0m"
    echo -e "\e[92m===============================================\e[0m"
    unset cmd
    while (true)
    do
      if [[ "${cmd}" == "" ]]
      then
        echo -e "\e[92m请选择你要更改的选项(修改完毕输入数字 0 确认修改并退出)：\e[0m\c"
        read cmd
      else
        break
      fi
    done
    case "${cmd}" in
      0)
      info "更改已保存！"
         break
         ;;
      *)
      changelist=($(sed -n ${cmd}p "${dst_cluster_file}"))
      if [ "${changelist[4]}" = "choose" ]
      then
        echo -e "\e[92m请选择${changelist[2]}：\e[0m\c"
        index=1
        for ((i=5;i<${#changelist[*]};i=$i+2))
        do
          echo -e "\e[92m${index}.${changelist[$[$i + 1]]}  \e[0m\c"
          index=$((${index} + 1))
        done
        echo -e "\e[92m: \e[0m\c"
        read changelistindex
        listnum=$(($((${changelistindex} - 1)) * 2))
        changelist[1]=${changelist[$[$listnum + 5]]}
      else
        echo -e "\e[92m请输入${changelist[2]}：\e[0m\c"
        read changestr
        # 处理空格
        changestr=$(echo "${changestr}" | sed 's/ /#/g')
        changelist[1]=${changestr}
      fi
      changestr=${changelist[@]}
      sed -i "${cmd}c ${changestr}" ${dst_cluster_file}
      ;;
    esac
    done
    type=([STEAM] [GAMEPLAY] [NETWORK] [MISC] [SHARD])
    for (( i=0; i<${#type[*]}; i++ ))
    do
    echo "${type[i]}" >> "${dst_base_dir}/${cluster}/cluster.ini"
    cat "${dst_cluster_file}" | grep -v "script_ver" | while read lc
    do
      lcstr=($lc)
      if [ "${lcstr[3]}" == "${type[i]}" ]
      then
        if [ "${lcstr[1]}" == "无" ]
        then
          lcstr[1]=""
        fi
        # 还原空格
        value_str=$(echo "${lcstr[1]}" | sed 's/#/ /g')
        echo "${lcstr[0]} = ${value_str}" >> "${dst_base_dir}/${cluster}/cluster.ini"
      fi
    done
    echo "" >> "${dst_base_dir}/${cluster}/cluster.ini"
    done
    # 暴食MOD不可以暂停
    if [ $(grep "^game_mode" ${dst_base_dir}/${cluster}/cluster.ini | cut -d " " -f3) == "quagmire" ]
    then
    str=$(grep "^pause_when_empty" ${dst_base_dir}/${cluster}/cluster.ini)
    newstr="pause_when_empty = fasle"
    sed -i "s/$str/$newstr/g" ${dst_base_dir}/${cluster}/cluster.ini
    fi
}

Set_token(){
    if [ -f "${dst_token_file}" ]
    then
    default_token=$(cat "${dst_token_file}")
    else
    default_token="pds-g^KU_6yNrwFkC^9WDPAGhDM9eN6y2v8UUjEL3oDLdvIkt2AuDQB2mgaGE="
    fi
    info "当前预设的服务器令牌：\n ${default_token}"
    echo -e "\e[92m是否更改？ 1.是  2.否 : \e[0m\c"
    read ch
    if [ $ch -eq 1 ]
    then
    tip "请输入或粘贴你的令牌到此处："
    read mytoken
    mytoken=$(echo "${mytoken}" | sed 's/ //g')
    echo "${mytoken}" > "${dst_token_file}"
    info "已更改服务器默认令牌！"
    else
    echo "${default_token}" > ${dst_token_file}
    fi
    cat "${dst_token_file}" > "${dst_base_dir}/${cluster}/cluster_token.txt"
}
Set_list(){
    if [ ! -f "${data_dir}/alist.txt" ]
    then
    touch "${data_dir}/alist.txt"
    fi
    if [ ! -f "${data_dir}/blist.txt" ]
    then
    touch "${data_dir}/blist.txt"
    fi
    if [ ! -f "${data_dir}/wlist.txt" ]
    then
    touch "${data_dir}/wlist.txt"
    fi
    cat "${data_dir}/alist.txt" > "${dst_base_dir}/${cluster}/adminlist.txt"
    cat "${data_dir}/blist.txt" > "${dst_base_dir}/${cluster}/blocklist.txt"
    cat "${data_dir}/wlist.txt" > "${dst_base_dir}/${cluster}/whitelist.txt"
}
Set_world(){
    if [[ "${shardtype}" == "熔炉MOD房[Forged Forge]" || "${shardtype}" == "挂机MOD房" || "${shardtype}" == "暴食MOD房" || "${shardtype}" == "熔炉MOD房[ReForged]" ]]
    then
    cat "${data_dir}/${Wconfigfile}" > "${dst_base_dir}/${cluster}/${sharddir}/leveldataoverride.lua"
    info "${shardtype}世界配置已写入！"
    info "正在检查${shardtype}MOD是否已下载安装 。。。"
    if [ -f "${dst_server_dir}/mods/workshop-${Wmodid}/modinfo.lua" ]
    then
      info "${shardtype}MOD已安装 。。。"
    else
      tip "${shardtype}MOD未安装 。。。即将下载 。。。"
      echo "ServerModSetup(\"${Wmodid}\")" > "${dst_server_dir}/mods/dedicated_server_mods_setup.lua"
      Download_MOD
    fi
    if [ -f "${dst_server_dir}/mods/workshop-${Wmodid}/modinfo.lua" ]
    then
      Default_mod
      modid=${Wmodid}
      Get_shard_array
      Addmodfunc
      info "${shardtype}MOD已启用 。。。"
    else
      tip "${shardtype}MOD启用失败，请自行检查原因或反馈 。。。"
    fi
    else
    info "是否修改${shardtype}[${sharddir}]配置？：1.是 2.否（默认为上次配置）"
    read wc
    configure_file="${data_dir}/${shardname}leveldata.txt"
    data_file="${dst_base_dir}/${cluster}/${sharddir}/leveldataoverride.lua"
    if [ "${wc}" -ne 2 ]
    then
      Set_world_config
    fi
    Write_in ${shardname}
    fi
}
Set_world_config(){
    while (true)
    do
    clear
    index=1
    linenum=1
    list=(environment source food animal monster)
    liststr=(
    ================================世界环境================================
    ==================================资源==================================
    ==================================食物==================================
    ==================================动物==================================
    ==================================怪物==================================
    )
    for ((j=0;j<${#list[*]};j++))
    do
      echo -e "\n\e[92m${liststr[$j]}\e[0m"
      cat "${configure_file}" | while read line
      do
        ss=(${line})
        if [ "${#ss[@]}" -gt 4 ]
        then
          if [ "${index}" -gt 3 ]
          then
            printf "\n"
            index=1
          fi
          for ((i=4;i<${#ss[*]};i++))
          do
            if [ "${ss[$i]}" == "${ss[1]}" ]
            then
              value=${ss[$i+1]}
            fi
          done
          if [ "${list[$j]}" == "${ss[2]}" ]
          then
            if [ ${linenum} -lt 10 ]
            then
              printf "%-21s\t" "[ ${linenum}]${ss[3]}: ${value}"
            else
              printf "%-21s\t" "[${linenum}]${ss[3]}: ${value}"
            fi
            index=$((${index} + 1))
          fi
        fi
        linenum=$((${linenum} + 1))
      done
    done
    printf "\n"
    unset cmd
    while (true)
    do
      if [[ "${cmd}" == "" ]]
      then
        echo -e "\e[92m请选择你要更改的选项(修改完毕输入数字 0 确认修改并退出)： \e[0m\c"
        read cmd
      else
        break
      fi
    done
    case "${cmd}" in
      0)
      info "更改已保存！"
      break
      ;;
      *)
      changelist=($(sed -n "${cmd}p" "${configure_file}"))
         echo -e "\e[92m请选择${changelist[3]}： \e[0m\c"
         index=1
         for ((i=4;i<${#changelist[*]};i=$i+2))
         do
           echo -e "\e[92m${index}.${changelist[$[$i + 1]]}   \e[0m\c"
           index=$[${index} + 1]
         done
         echo -e "\e[92m: \e[0m\c"
         read changelistindex
         listnum=$[${changelistindex} - 1]*2
         changelist[1]=${changelist[$[$listnum + 4]]}
         changestr="${changelist[@]}"
         sed -i "${cmd}c ${changestr}" "${configure_file}";;
    esac
    done
}
Write_in(){
    data_num=$(grep -n "^" "${configure_file}" | tail -n 1 | cut -d : -f1)
    cat "${data_dir}/${1}start.lua" > "${data_file}"
    index=1
    cat "${configure_file}" | while read line
    do
    ss=(${line})
    if [ "${index}" -lt "${data_num}" ]
    then
      char=","
    else
      char=""
    fi
    index=$[${index} + 1]
    if [[ "${ss[1]}" == "highlyrandom" ]]
    then
      str="${ss[0]}=\"highly random\"${char}"
    else
      str="[\"${ss[0]}\"]=\"${ss[1]}\"${char}"
    fi
    echo "    ${str}" >> "${data_file}"
    done
    cat "${data_dir}/${1}end.lua" >> "${data_file}"
}
Default_mod(){
    Get_shard_array
    for shard in ${shardarray}
    do
    if [ ! -f "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua" ]
    then
      echo 'return {
}' > "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua"
    fi
    done
}
Setup_mod(){
    if [ -f "${data_dir}/mods_setup.lua" ]
    then
    rm -rf "${data_dir}/mods_setup.lua"
    fi
    touch "${data_dir}/mods_setup.lua"
    Get_single_shard
    dir=$(cat "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua" | grep "workshop" | cut -f2 -d '"' | cut -d "-" -f2)
    for moddir in ${dir}
    do
    if [ $(grep "${moddir}" -c "${data_dir}/mods_setup.lua") -eq 0 ]
    then
      if checkmodupdate ${moddir}
      then
		echo "ServerModSetup(\"${moddir}\")" >> "${data_dir}/mods_setup.lua"
      fi
    fi
    done
    cp "${data_dir}/mods_setup.lua" "${dst_server_dir}/mods/dedicated_server_mods_setup.lua"
    info "添加启用的MODID到MOD更新配置文件！"
}
Start_shard(){
    Setup_mod
    Backup_cluster
    Save_log
    cd "${dst_server_dir}/bin"
    for shard in ${shardarray}
    do
    unset TMUX
    tmux new-session -s DST_${shard} -d "${dst_bin_cmd} -persistent_storage_root ${dst_conf_basedir} -conf_dir ${dst_conf_dirname} -cluster ${cluster} -shard ${shard}"
    done
}
Save_log(){
    Clean_old_log
    Get_single_shard
    if [ -f "$dst_base_dir/$cluster/$shard/server_chat_log.txt" ]
    then
    cur_day=$(date "+%F")
    if [ ! -d "$log_save_dir/$cur_day" ]
    then
      mkdir -p "$log_save_dir/$cur_day"
    fi
    cur_time=$(date "+%H%M%S")
    echo "$(date)" >> "$log_save_dir/$cur_day/server_chat_log_backup_${cluster}_${shard}_${cur_time}.txt"
    cp "$dst_base_dir/$cluster/$shard/server_chat_log.txt" "$log_save_dir/$cur_day/server_chat_log_backup_${cluster}_${shard}_${cur_time}.txt"
    echo "$(date)" >> "$log_save_dir/$cur_day/server_log_backup_${cluster}_${shard}_${cur_time}.txt"
    cp  "$dst_base_dir/$cluster/$shard/server_log.txt" "$log_save_dir/$cur_day/server_log_backup_${cluster}_${shard}_${cur_time}.txt"
    info "【${shard}】旧的日志已备份到\n       ==>【$log_save_dir/$cur_day】"
    info "【保留一周内的日志备份】。"
    fi
}
Clean_old_log(){
    # 保留一周的日志
    all=$(ls $log_save_dir | grep -c ^)
    if [ $all -gt 6 ]
    then
    info "清理旧的备份日志 ..."
    del=$(($all - 7))
    for dir in $(ls $log_save_dir | sort | head -n $del)
    do
      rm -rf $log_save_dir/$dir
    done
    fi
}
Backup_cluster(){
    Clean_old_cluster
    Get_current_cluster
    Get_single_shard
    if [ -d "$dst_base_dir/$cluster/$shard/save" ]
    then
    cur_day=$(date "+%F")
    if [ ! -d "$cluster_backup_dir/$cur_day" ]
    then
      mkdir -p "$cluster_backup_dir/$cur_day"
    fi
    cur_time=$(date "+%H%M%S")
    tar -zcPf "$cluster_backup_dir/$cur_day/cluster_backup_${cluster}_${cur_time}.tar.gz" "$dst_base_dir/$cluster"
    info "【${shard}】旧的存档已备份到\n       ==>【$cluster_backup_dir/$cur_day】"
    info "【保留三天内的存档备份】。"
    fi
}
Clean_old_cluster(){
    # 保留三天的存档备份
    if [ ! -d "$cluster_backup_dir" ]
    then
    mkdir -p "$cluster_backup_dir"
    fi
    all=$(ls $cluster_backup_dir | grep -c ^)
    if [ $all -gt 2 ]
    then
    info "清理旧的存档备份 ..."
    del=$(($all - 2))
    for dir in $(ls $cluster_backup_dir | sort | head -n $del)
    do
      rm -rf $cluster_backup_dir/$dir
    done
    fi
}
Pid_kill(){
    kill $(ps -ef | grep -v grep | grep $1 | awk '{print $2}')
}
Start_check(){
    Get_shard_array
    rm "${ays_log_file}" >/dev/null 2>&1
    touch "${ays_log_file}"
    shardnum=0
    for shard in $shardarray
    do
    unset TMUX
    tmux new-session -s DST_"${shard}"_log -d "bash ${HOME}/dstserver.sh ay $shard"
    shardnum=$[$shardnum + 1]
    done
    ANALYSIS_SHARD=0
    any_log_index=1
    unset any_old_line
    while (true)
    do
    if [ "$ANALYSIS_SHARD" -lt $shardnum ]
    then
      anyline=$(sed -n ${any_log_index}p ${ays_log_file})
      if [[ "$anyline" != "" && "$anyline" != "$any_old_line" ]]
      then
        any_log_index=$(($any_log_index + 1))
        any_old_line=$anyline
        if [ $(echo "$anyline" | grep -c ANALYSISLOGDONE) -gt 0 ]
        then
          ANALYSIS_SHARD=$(($ANALYSIS_SHARD + 1))
        else
          info "$anyline"
        fi
      fi
    else
      break
    fi
    done
}
printf_and_save_log(){
    printf "%-7s：%s\n" "$1" "$2" | tee -a $3
}
Analysis_log(){
    log_file="${dst_base_dir}/${cluster}/$1/server_log.txt"
    cat ${log_arr_str} > "${data_dir}/log_arr_str_$1.txt"
    if [ -f "$log_file" ]
    then
    RES="nodone"
    retrytime=0
    while [ $RES == "nodone" ]
    do
      while read line
      do
        line_0=$(echo $line | cut -d '@' -f1)
        line_1=$(echo $line | cut -d '@' -f2)
        line_2=$(echo $line | cut -d '@' -f3)
        if [ $(grep "$line_1" -c $log_file) -gt 0 ]
        then
          case "$line_0" in
            1)
            printf_and_save_log $1 $line_2 "$ays_log_file"
            RES="done"
            printf_and_save_log $1 "ANALYSISLOGDONE" "$ays_log_file"
            break;;
            *)
            if [ $(grep ".*Connection to master failed. Waiting to reconnect.*" -c $log_file) -gt 0 ]
            then
              retrytime=$[$retrytime + 1]
              if [ $retrytime -le 5 ]
              then
                printf_and_save_log $1 "连接失败！第$retrytime次连接重试！" "$ays_log_file"
                sleep 10
              fi
            fi
            printf_and_save_log "$1" "$line_2" "$ays_log_file"
            num=$(grep "$line_2" -n "${data_dir}/log_arr_str_$1.txt" | cut -d ":" -f1)
            sed -i "${num}d" "${data_dir}/log_arr_str_$1.txt"
            break;;
          esac
        fi
      done < "${data_dir}/log_arr_str_$1.txt"
    done
    fi
}
#############################################################################
First_run_check(){
    Open_swap
    Mkdstdir
    if [ ! -f "${dst_server_dir}/version.txt" ]
    then
    Initfiles
    info "检测到你是首次运行脚本，需要进行必要的配置，所需时间由服务器带宽决定，大概一个小时 ..."
    Install_Dependency
    Install_Steamcmd
    info "安装游戏服务端 ..."
    Install_Game
    Fix_steamcmd
    if [ ! -f "${dst_server_dir}/version.txt" ]
    then
      error "安装失败，请重试！多次重试仍无效请反馈!" && exit 1
    fi
    info "首次运行配置完毕，你可以创建新的世界了。"
    fi
}
Initfiles(){
    cat > $data_dir/aog.lua <<-EOF
return {
  desc="别傻了，还是充钱来的实在！！！",
  hideminimap=false,
  id="Auto_Open_Gift",
  location="forest",
  max_playlist_position=9,
  min_playlist_position=0,
  name="偷渡欧洲宝地--由脚本dstserver.sh创建！",
  numrandom_set_pieces=0,
  ordered_story_setpieces={  },
  override_level_string=false,
  ["overrides"]={
    ["alternatehunt"]="never",
    ["angrybees"]="never",
    ["antliontribute"]="never",
    ["autumn"]="never",
    ["bearger"]="never",
    ["beefalo"]="never",
    ["beefaloheat"]="never",
    ["bees"]="never",
    ["berrybush"]="never",
    ["birds"]="never",
    ["boons"]="never",
    ["branching"]="never",
    ["butterfly"]="never",
    ["buzzard"]="never",
    ["cactus"]="never",
    ["carrot"]="never",
    ["catcoon"]="never",
    ["chess"]="never",
    ["day"]="onlyday",
    ["deciduousmonster"]="never",
    ["deerclops"]="never",
    ["disease_delay"]="none",
    ["dragonfly"]="never",
    ["flint"]="never",
    ["flowers"]="never",
    ["frograin"]="never",
    ["goosemoose"]="never",
    ["grass"]="never",
    ["has_ocean"]=true,
    ["houndmound"]="never",
    ["hounds"]="never",
    ["hunt"]="never",
    ["keep_disconnected_tiles"]=true,
    ["krampus"]="never",
    ["layout_mode"]="LinkNodesByKeys",
    ["liefs"]="never",
    ["lightning"]="never",
    ["lightninggoat"]="never",
    ["loop"]="never",
    ["lureplants"]="never",
    ["marshbush"]="never",
    ["merm"]="never",
    ["meteorshowers"]="never",
    ["meteorspawner"]="never",
    ["moles"]="never",
    ["mushroom"]="never",
    ["no_joining_islands"]=true,
    ["no_wormholes_to_disconnected_tiles"]=true,
    ["penguins"]="never",
    ["perd"]="never",
    ["petrification"]="none",
    ["pigs"]="never",
    ["ponds"]="never",
    ["prefabswaps_start"]="classic",
    ["rabbits"]="never",
    ["reeds"]="never",
    ["regrowth"]="veryslow",
    ["roads"]="never",
    ["rock"]="never",
    ["rock_ice"]="never",
    ["sapling"]="never",
    ["season_start"]="autumn",
    ["specialevent"]="auto",
    ["spiders"]="never",
    ["spring"]="noseason",
    ["start_location"]="default",
    ["summer"]="noseason",
    ["tallbirds"]="never",
    ["task_set"]="Auto_Open_Gift",
    ["tentacles"]="never",
    ["touchstone"]="never",
    ["trees"]="never",
    ["tumbleweed"]="never",
    ["walrus"]="never",
    ["weather"]="never",
    ["wildfires"]="never",
    ["winter"]="noseason",
    ["world_size"]="small",
    ["wormhole_prefab"]="wormhole"
  },
  ["random_set_pieces"]={},
  ["required_prefabs"]={ "multiplayer_portal" },
  ["substitutes"]={},
  ["version"]=4
}
EOF

cat > $data_dir/Cavesend.lua <<-EOF
  },
  required_prefabs={ "multiplayer_portal" },
  substitutes={  },
  version=4
}
EOF

cat > $data_dir/Cavesstart.lua <<-EOF
return {
  background_node_range={ 0, 1 },
  desc="由脚本dstserver.sh创建！",
  hideminimap=false,
  id="DST_CAVE",
  location="cave",
  max_playlist_position=999,
  min_playlist_position=0,
  name="洞穴探险--由脚本dstserver.sh创建！",
  numrandom_set_pieces=0,
  override_level_string=false,
  overrides={
EOF

cat > $data_dir/Cavesleveldata.txt <<-EOF
boons default environment 前辈遗迹 never 无 rare 较少 default 默认 often 较多 always 大量
branching default environment 岔路地形 never 无 least 最少 default 默认 most 最多
cavelight default environment 洞穴光照 veryslow 极慢 slow 慢 default 默认 fast 快 veryfast 极快
disease_delay default environment 作物患病 none 无 random 随机 long 慢 default 默认 short 快
earthquakes default environment 地震频率 never 无 rare 较少 default 默认 often 较多 always 大量
loop default environment 环状地形 never 无 least 最少 default 默认 most 最多
petrification default environment 石化速率 none 无 few 慢 default 默认 many 快 max 极快
regrowth default environment 资源再生 veryslow 极慢 slow 慢 default 默认 fast 快 veryfast 极快
touchstone default environment 猪头祭坛 never 无 rare 较少 default 默认 often 较多 always 大量
weather default environment 雨 never 无 rare 较少 default 默认 often 较多 always 大量
world_size default environment 地图大小 small 小型 medium 中等 huge 巨型 default 大型
wormlights default environment 发光浆果 never 无 rare 较少 default 默认 often 较多 always 大量
roads never environment 道路  never 无 default 默认
prefabswaps_start default environment 初始多样性 classic 经典 highlyrandom 高度随机 default 默认
fern default source 蕨类植物 never 无 rare 较少 default 默认 often 较多 always 大量
flint default source 燧石 never 无 rare 较少 default 默认 often 较多 always 大量
flower_cave default source 荧光花 never 无 rare 较少 default 默认 often 较多 always 大量
grass default source 草 never 无 rare 较少 default 默认 often 较多 always 大量
marshbush default source 荆棘灌木 never 无 rare 较少 default 默认 often 较多 always 大量
mushtree default source 蘑菇树 never 无 rare 较少 default 默认 often 较多 always 大量
reeds default source 芦苇 never 无 rare 较少 default 默认 often 较多 always 大量
rock default source 岩石 never 无 rare 较少 default 默认 often 较多 always 大量
sapling default source 树枝 never 无 rare 较少 default 默认 often 较多 always 大量
trees default source 树木 never 无 rare 较少 default 默认 often 较多 always 大量
banana default food 香蕉 never 无 rare 较少 default 默认 often 较多 always 大量
berrybush often food 浆果丛 never 无 rare 较少 default 默认 often 较多 always 大量
lichen default food 苔藓 never 无 rare 较少 default 默认 often 较多 always 大量
mushroom default food 蘑菇 never 无 rare 较少 default 默认 often 较多 always 大量
bunnymen default animal 兔人 never 无 rare 较少 default 默认 often 较多 always 大量
cave_ponds default animal 洞穴池塘 never 无 rare 较少 default 默认 often 较多 always 大量
monkey default animal 猴子 never 无 rare 较少 default 默认 often 较多 always 大量
rocky default animal 石虾 never 无 rare 较少 default 默认 often 较多 always 大量
slurper default animal 啜食者 never 无 rare 较少 default 默认 often 较多 always 大量
slurtles default animal 蜗牛 never 无 rare 较少 default 默认 often 较多 always 大量
bats rare monster 蝙蝠 never 无 rare 较少 default 默认 often 较多 always 大量
cave_spiders default monster 洞穴蜘蛛 never 无 rare 较少 default 默认 often 较多 always 大量
chess default monster 齿轮怪 never 无 rare 较少 default 默认 often 较多 always 大量
fissure default monster 影怪裂缝 never 无 rare 较少 default 默认 often 较多 always 大量
liefs default monster 树精 never 无 rare 较少 default 默认 often 较多 always 大量
tentacles rare monster 触手怪 never 无 rare 较少 default 默认 often 较多 always 大量
wormattacks default monster 蠕虫袭击 never 无 rare 较少 default 默认 often 较多 always 大量
worms default monster 蠕虫 never 无 rare 较少 default 默认 often 较多 always 大量
layout_mode RestrictNodesByKey other 其他
start_location caves other 其他
task_set cave_default other 其他
wormhole_prefab tentacle_pillar other 其他
EOF

cat > $data_dir/clusterdata.txt <<-EOF
cluster_name 由脚本dstserver.sh创建！ 房间名称 [NETWORK] read
cluster_description 由脚本dstserver.sh创建！ 房间简介 [NETWORK] read
cluster_intention social 游戏风格 [NETWORK] choose social 休闲 cooperative 合作 competitive 竞赛 madness 疯狂
game_mode survival 游戏模式 [GAMEPLAY] choose endless 无尽 survival 生存 wilderness 荒野 lavaarena 熔炉 quagmire 暴食
cluster_language zh 游戏语言 [NETWORK] choose zh 简体中文 en 英语
steam_group_id 0 Steam群组ID [STEAM] read
steam_group_admins false 群组官员设为管理员 [STEAM] choose true 开启 false 关闭
steam_group_only false 仅群组成员可进 [STEAM] choose true 开启 false 关闭
pause_when_empty true 无人暂停 [GAMEPLAY] choose true 开启 false 关闭
vote_enabled true 投票 [GAMEPLAY] choose true 开启 false 关闭
pvp false PVP竞技 [GAMEPLAY] choose true 开启 false 关闭
whitelist_slots 0 房间预留位置个数 [NETWORK] read
idle_timeout 0 挂机超时踢出时间 [NETWORK] read
cluster_password 无 房间密码[设无密码请输入无！！！] [NETWORK] read
max_players 6 最大玩家人数 [GAMEPLAY] read
master_ip 127.0.0.1 主世界IP(多服务器必须修改此项) [SHARD] read
lan_only_cluster false 仅局域网 [NETWORK] readonly
offline_cluster false 离线模式 [NETWORK] readonly
autosaver_enabled true 自动保存 [NETWORK] readonly
tick_rate 15 主客机同步频率 [NETWORK] readonly
max_snapshots 10 最大存档快照数 [MISC] readonly
console_enabled true 控制台 [MISC] readonly
shard_enabled true 多世界 [SHARD] readonly
bind_ip 0.0.0.0 绑定IP [SHARD] readonly
master_port 10888 游戏端口 [SHARD] readonly
cluster_key Ariwori 多世界通信秘钥 [SHARD] readonly
EOF

cat > $data_dir/Forestend.lua <<-EOF
},
  ["random_set_pieces"]={
    "Sculptures_2",
    "Sculptures_3",
    "Sculptures_4",
    "Sculptures_5",
    "Chessy_1",
    "Chessy_2",
    "Chessy_3",
    "Chessy_4",
    "Chessy_5",
    "Chessy_6",
    "Maxwell1",
    "Maxwell2",
    "Maxwell3",
    "Maxwell4",
    "Maxwell6",
    "Maxwell7",
    "Warzone_1",
    "Warzone_2",
    "Warzone_3"
  },
  ["required_prefabs"]={ "multiplayer_portal" },
  ["required_setpieces"]={ "Sculptures_1", "Maxwell5" },
  ["substitutes"]={},
  ["version"]=4
}
EOF

cat > $data_dir/Foreststart.lua <<-EOF
return {
  ["desc"]="由脚本dstserver.sh创建！",
  ["hideminimap"]=false,
  id="SURVIVAL_TOGETHER",
  ["location"]="forest",
  ["max_playlist_position"]=999,
  ["min_playlist_position"]=0,
  ["name"]="游山玩水--由脚本dstserver.sh创建！",
  ["numrandom_set_pieces"]=4,
  ["override_level_string"]=false,
  overrides={
    ["has_ocean"]=true,
  ["no_joining_islands"]=true,
    ["no_wormholes_to_disconnected_tiles"]=true,
    ["keep_disconnected_tiles"]=true,
EOF

cat > $data_dir/Forestleveldata.txt <<-EOF
autumn default environment 秋天 noseason 无 veryshortseason 很短 shortseason 短 longseason 长 verylongseason 很长 random 随机 default 默认
boons default environment 前辈遗迹 never 无 rare 较少 default 默认 often 较多 always 大量
branching default environment 岔路地形 never 无 least 最少 default 默认 most 最多
day default environment 昼夜长短 longday 长白昼 longdusk 长黄昏 longnight 长夜晚 noday 无白昼 nodusk 无黄昏 nonight 无夜晚 onlyday 仅白昼 onlydusk 仅黄昏 onlynight 仅夜晚
disease_delay default environment 作物患病 none 无 random 随机 long 慢 default 默认 short 快
frograin default environment 青蛙雨 never 无 rare 较少 default 默认 often 较多 always 大量
lightning default environment 闪电 never 无 rare 较少 default 默认 often 较多 always 大量
loop default environment 环状地形 never 无 least 最少 default 默认 most 最多
petrification default environment 石化速率 none 无 few 慢 default 默认 many 快 max 极快
regrowth default environment 资源再生 veryslow 极慢 slow 慢 default 默认 fast 快 veryfast 极快
season_start default environment 初始季节 default 秋季 winter 冬季 spring 春季 summer 夏季 autumnorspring 秋或春 winterorsummer 冬或夏 random 随机
specialevent default environment 节日活动 none 无 default 自动 hallowed_nights 万圣夜 winters_feast 冬季盛宴 year_of_the_gobbler 鸡年活动 year_of_the_varg 狗年活动 year_of_the_pig 猪王年
spring default environment 春天 noseason 无 veryshortseason 很短 shortseason 短 longseason 长 verylongseason 很长 random 随机 default 默认
start_location default environment 初始环境 plus 三箱 darkness 永夜 default 默认
summer default environment 夏天 noseason 无 veryshortseason 很短 shortseason 短 longseason 长 verylongseason 很长 random 随机 default 默认
touchstone default environment 猪头祭坛 never 无 rare 较少 default 默认 often 较多 always 大量
weather default environment 雨 never 无 rare 较少 default 默认 often 较多 always 大量
wildfires default environment 自燃 never 无 rare 较少 default 默认 often 较多 always 大量
winter default environment 冬天 noseason 无 veryshortseason 很短 shortseason 短 longseason 长 verylongseason 很长 random 随机 default 默认
world_size default environment 地图大小 small 小型 medium 中等 huge 巨型 default 大型
roads default environment 道路 never 无 default 默认
task_set default environment 生物群落 classic 没有巨人 default 联机
prefabswaps_start default environment 初始多样性 classic 经典 highlyrandom 高度随机 default 默认
alternatehunt default source 动物脚印 never 无 rare 较少 default 默认 often 较多 always 大量
flint default source 燧石 never 无 rare 较少 default 默认 often 较多 always 大量
flowers default source 花 never 无 rare 较少 default 默认 often 较多 always 大量
grass default source 草 never 无 rare 较少 default 默认 often 较多 always 大量
marshbush default source 荆棘灌木 never 无 rare 较少 default 默认 often 较多 always 大量
meteorshowers default source 陨石区域 never 无 rare 较少 default 默认 often 较多 always 大量
meteorspawner default source 陨石频率 never 无 rare 较少 default 默认 often 较多 always 大量
ponds default source 池塘 never 无 rare 较少 default 默认 often 较多 always 大量
reeds default source 芦苇 never 无 rare 较少 default 默认 often 较多 always 大量
rock default source 岩石 never 无 rare 较少 default 默认 often 较多 always 大量
rock_ice default source 冰川 never 无 rare 较少 default 默认 often 较多 always 大量
sapling default source 树枝 never 无 rare 较少 default 默认 often 较多 always 大量
trees default source 树木 never 无 rare 较少 default 默认 often 较多 always 大量
tumbleweed default source 风滚草 never 无 rare 较少 default 默认 often 较多 always 大量
berrybush default food 浆果丛 never 无 rare 较少 default 默认 often 较多 always 大量
cactus default food 仙人掌 never 无 rare 较少 default 默认 often 较多 always 大量
carrot default food 胡萝卜 never 无 rare 较少 default 默认 often 较多 always 大量
mushroom default food 蘑菇 never 无 rare 较少 default 默认 often 较多 always 大量
angrybees default animal 杀人蜂 never 无 rare 较少 default 默认 often 较多 always 大量
beefalo default animal 皮费罗牛 never 无 rare 较少 default 默认 often 较多 always 大量
bees default animal 蜜蜂 never 无 rare 较少 default 默认 often 较多 always 大量
birds default animal 鸟 never 无 rare 较少 default 默认 often 较多 always 大量
butterfly default animal 蝴蝶 never 无 rare 较少 default 默认 often 较多 always 大量
buzzard default animal 秃鹫 never 无 rare 较少 default 默认 often 较多 always 大量
catcoon default animal 浣猫 never 无 rare 较少 default 默认 often 较多 always 大量
hunt default animal 狼/羊/象 never 无 rare 较少 default 默认 often 较多 always 大量
lightninggoat default animal 电羊 never 无 rare 较少 default 默认 often 较多 always 大量
moles default animal 鼹鼠 never 无 rare 较少 default 默认 often 较多 always 大量
penguins default animal 企鹅 never 无 rare 较少 default 默认 often 较多 always 大量
perd default animal 火鸡 never 无 rare 较少 default 默认 often 较多 always 大量
pigs default animal 猪人 never 无 rare 较少 default 默认 often 较多 always 大量
rabbits default animal 兔子 never 无 rare 较少 default 默认 often 较多 always 大量
tallbirds default animal 高脚鸟 never 无 rare 较少 default 默认 often 较多 always 大量
beefaloheat default animal 牛发情频率 never 无 rare 较少 default 默认 often 较多 always 大量
antliontribute default monster 蚁狮事件 never 无 rare 较少 default 默认 often 较多 always 大量
bearger rare monster 熊 never 无 rare 较少 default 默认 often 较多 always 大量
chess default monster 齿轮怪 never 无 rare 较少 default 默认 often 较多 always 大量
deciduousmonster default monster 桦树精 never 无 rare 较少 default 默认 often 较多 always 大量
deerclops default monster 独眼巨鹿 never 无 rare 较少 default 默认 often 较多 always 大量
dragonfly default monster 龙蝇 never 无 rare 较少 default 默认 often 较多 always 大量
goosemoose default monster 鹿角鹅 never 无 rare 较少 default 默认 often 较多 always 大量
houndmound default monster 猎犬丘 never 无 rare 较少 default 默认 often 较多 always 大量
hounds default monster 猎犬袭击 never 无 rare 较少 default 默认 often 较多 always 大量
krampus default monster 坎普斯 never 无 rare 较少 default 默认 often 较多 always 大量
liefs default monster 树精 never 无 rare 较少 default 默认 often 较多 always 大量
lureplants default monster 食人花 never 无 rare 较少 default 默认 often 较多 always 大量
merm default monster 鱼人 never 无 rare 较少 default 默认 often 较多 always 大量
spiders default monster 蜘蛛 never 无 rare 较少 default 默认 often 较多 always 大量
tentacles default monster 触手怪 never 无 rare 较少 default 默认 often 较多 always 大量
walrus default monster 海象 never 无 rare 较少 default 默认 often 较多 always 大量
layout_mode LinkNodesByKeys other 其他
wormhole_prefab wormhole other 虫洞生物
EOF

cat > $data_dir/quagmire.lua <<-EOF
return {
  background_node_range={ 0, 0 },
  desc="你能经受暴食的挑战吗？--由脚本dstserver.sh创建！",
  hideminimap=false,
  id="QUAGMIRE",
  location="quagmire",
  max_playlist_position=999,
  min_playlist_position=0,
  name="暴食：你会做饭吗？--由脚本dstserver.sh创建！",
  numrandom_set_pieces=0,
  override_level_string=false,
  overrides={
    boons="never",
    branching="random",
    disease_delay="none",
    keep_disconnected_tiles=false,
    layout_mode="RestrictNodesByKey",
    loop_percent=0,
    no_joining_islands=true,
    no_wormholes_to_disconnected_tiles=true,
    petrification="none",
    poi="never",
    prefabswaps_start="classic",
    protected="never",
    roads="never",
    season_start="default",
    start_location="quagmire_startlocation",
    task_set="quagmire_taskset",
    touchstone="never",
    traps="never",
    wildfires="never",
    world_size="small"
  },
  required_prefabs={ "quagmire_portal" },
  substitutes={  },
  version=4
}
EOF

cat > $data_dir/lavaarena.lua <<-EOF
return {
    background_node_range={ 0, 1 },
    desc="由脚本dstserver.sh创建！",
    hideminimap=false,
    id="LAVAARENA",
    location="lavaarena",
    max_playlist_position=999,
    min_playlist_position=0,
    name="熔炉斗兽场--由脚本dstserver.sh创建！",
    numrandom_set_pieces=0,
    override_level_string=false,
    overrides={
      has_ocean=false,
      boons="never",
      keep_disconnected_tiles=true,
      layout_mode="RestrictNodesByKey",
      poi="never",
      protected="never",
      roads="never",
      season_start="default",
      start_location="lavaarena",
      task_set="lavaarena_taskset",
      touchstone="never",
      traps="never",
      world_size="small"
    },
    required_prefabs={ "lavaarena_portal" },
    substitutes={  },
    version=4
  }
EOF

cat > $data_dir/lavaarena1.lua <<-EOF
return {
  ["background_node_range"]={ 0, 1 },
  ["desc"]="你敢进入熔炉证明自己吗？",
  ["hideminimap"]=false,
  id="LAVAARENA",
  ["location"]="lavaarena",
  ["max_playlist_position"]=999,
  ["min_playlist_position"]=0,
  ["name"]="熔炉斗兽场--由脚本dstserver.sh创建！",
  ["numrandom_set_pieces"]=0,
  ["override_level_string"]=false,
  ["overrides"]={
    ["boons"]="never",
    ["keep_disconnected_tiles"]=true,
    ["layout_mode"]="RestrictNodesByKey",
    ["no_joining_islands"]=true,
    ["no_wormholes_to_disconnected_tiles"]=true,
    ["poi"]="never",
    ["protected"]="never",
    ["roads"]="never",
    ["season_start"]="default",
    ["start_location"]="lavaarena",
    ["task_set"]="lavaarena_taskset",
    ["touchstone"]="never",
    ["traps"]="never",
    ["world_size"]="small" 
  },
  ["required_prefabs"]={ "lavaarena_portal" },
  ["substitutes"]={  },
  ["version"]=4 
}
EOF

cat > $data_dir/logarr.txt <<-EOF
0@.*Mounting file system databundles/scripts.zip successful.*@加载游戏文件完成。。。
0@.*OnLoadUserIdList: .*DoNotStarveTogether.*@加载房间配置完成。。。
0@.*GameSpecific initialize: Okay.*@开始运行服务端程序。。。
0@.*DownloadMods.*@开始下载或更新MOD并加载MOD配置，MOD多/大这里会卡久，请耐心等。。。
0@.*Online Server Started on port: .*@开始收集服务器配置。。。
0@.*Generating SURVIVAL Mode Level.*@正在创建世界。。。
0@.*About to start a shard with these settings:.*@正在连接世界。。。
1@.*World .* is now connected.*@世界连接成功。。。服务器开启成功！
1@.*Your Server Will Not Start.*@令牌缺失。。。服务器开启失败！
1@.*SOCKET_PORT_ALREADY_IN_USE.*@端口冲突。。。服务器开启失败！
1@.*LUA is now ready!.*@服务器开启成功！
1@.*Sim paused.*@世界运行暂停。。。服务器开启成功！
1@.*Registering master server.*@服务器开启成功！
EOF

cat > $data_dir/modconf.lua <<-EOF
require "modinfo"

-- Addon function
function trim(s)
    return (string.gsub(s, "^%s*(.-)%s*$", "%1"))
end

function LuaRemove(str,remove)
    local lcSubStrTab = {}
    while true do
    local lcPos = string.find(str,remove)
    if not lcPos then
      lcSubStrTab[#lcSubStrTab+1] =  str
      break
    end
    local lcSubStr  = string.sub(str,1,lcPos-1)
    lcSubStrTab[#lcSubStrTab+1] = lcSubStr
    str = string.sub(str,lcPos+1,#str)
    end
    local lcMergeStr =""
    local lci = 1
    while true do
    if lcSubStrTab[lci] then
      lcMergeStr = lcMergeStr .. lcSubStrTab[lci]
      lci = lci + 1
    else
      break
    end
    end
    return lcMergeStr
end
function Blank2jin(str)
    return (string.gsub(str, " ", "#"))
end
---
function list()
    if used == "true" then
    used = "[已启用]:"
    else
    used = "[未启用]:"
    end
    if modid == nil then
    modid = "unknown"
    end
    if name ~= nil then
    name = trim(name)
    name = LuaRemove(name, "\n")
    else
    name = "Unknown"
    end
    if configuration_options ~= nil and #configuration_options > 0 then
    cfg = "[可配置]:"
    else
    cfg = "[无配置]:"
    end
    local f = assert(io.open("modconflist.lua", 'a'))
    f:write(used, cfg, modid, ":", name, "\n")
    f:close()
end

function getver()
    print(version)
end

function table2json(t)
    local function serialize(tbl)
    local tmp = {}
    for k, v in pairs(tbl) do
      local k_type = type(k)
      local v_type = type(v)
      local key = (k_type == "string" and "\"" .. k .. "\":")
        or (k_type == "number" and "")
      local value = (v_type == "table" and serialize(v))
        or (v_type == "boolean" and tostring(v))
        or (v_type == "string" and "\"" .. v .. "\"")
        or (v_type == "number" and v)
        tmp[#tmp + 1] = key and value and tostring(key) .. tostring(value) or nil
    end
    if table.maxn(tbl) == 0 then
      return "{" .. table.concat(tmp, ",") .. "}"
    else
      return "[" .. table.concat(tmp, ",") .. "]"
    end
    end
    assert(type(t) == "table")
    return serialize(t)
end

function getname()
    if name then
    name = trim(name)
    name = LuaRemove(name, "\n")
    else
    name = "unknown"
    end
    print(name)
end

function createmodcfg()
    fname = "modconfigure/" .. modid .. ".cfg"
    local f = assert(io.open(fname, 'w'))
    f:write("mod-version = " .. version .. "\n")
    if name ~= nil then
    name = trim(name)
    name = Blank2jin(name)
    name = LuaRemove(name, "\n")
    end
    f:write("mod-name = " .. name .. "\n")
    if configuration_options ~= nil and #configuration_options > 0 then
    f:write("mod-configureable = true\n")
    for i, j in pairs(configuration_options) do
      if j.default == nil then
        if j.options ~= nil and #j.options > 0 then
          j.default = j.options[1].data
        end
      end
      if j.default ~= nil then
        local label = "nolabel"
        if j.label ~= nil then
          if string.len(j.label) >= 2 then
            label = Blank2jin(j.label)
            label = LuaRemove(label, "\n")
          end
        end
        local hover = "该项没有简介！"
        if j.hover ~= nil then
          if string.len(j.hover) >= 2 then
            hover = Blank2jin(j.hover)
            hover = LuaRemove(hover, "\n")
          end
        end
        local cfgname = Blank2jin(j.name)
        cfgname = LuaRemove(cfgname, "\n")
        if type(j.default) == "table" then
          f:write(cfgname .. " 表数据请直接修改modinfo.lua文件 table " .. label .. " " .. hover .. "\n")
        else
          f:write(cfgname .. " " .. tostring(j.default) .. " " .. type(j.default) .. " " .. label .. " " .. hover .. " ")
          if j.options ~= nil and #j.options > 0 then
            for k, v in pairs(j.options) do
              if type(v.data) ~= "table" then
                local description = ""
                if v.description ~= nil then
                  if string.len(v.description) >= 2 then
                    description = Blank2jin(v.description)
                    description = LuaRemove(description, "\n")
                  end
                end
                if description == "" then
                  description = tostring(v.data)
                end
                local cfghover = "该项没有说明！"
                if v.hover ~= nil then
                  if string.len(v.hover) >= 2 then
                    cfghover = v.hover
                  end
                end
                cfghover = Blank2jin(cfghover)
                cfghover = LuaRemove(cfghover, "\n")
                f:write(tostring(v.data) .. " " .. description .. " " .. cfghover)
              end
              if k ~= #j.options then
                f:write(" ")
              else
                f:write("\n")
              end
            end
          end
        end
      end
    end
    else
    f:write("mod-configureable = false\n")
    end
    f:close()
end
---------------------------------
if fuc == "list" then
    list()
elseif fuc == "getver" then
    getver()
elseif fuc == "getname" then
    getname()
elseif fuc == "createmodcfg" then
    createmodcfg()
end
EOF
}
Reset_data(){
    Initfiles
    info "已重置脚本数据！"
}
# open swap
Open_swap(){
  if [ $(free -m | grep -i swap | tr -cd [0-9]) == "000" ]
  then
    if [ ! -f "/swapfile" ]
    then
      info "创建虚拟内存 ..."
      sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
      sudo mkswap /swapfile
      sudo chmod 0600 /swapfile
      # 开机自启
      sudo chmod 0666 /etc/fstab
      echo "/swapfile swap swap defaults 0 0" >> /etc/fstab
      sudo chmod 0644 /etc/fstab
    fi
  fi
  if [ $(free -m | grep -i swap | tr -cd [0-9]) == "000" ]
  then
    sudo swapon /swapfile
    info "虚拟内存已开启！"
  fi
}
# 创建文件夹
Mkdstdir(){
    mkdir -p "${DST_HOME}/steamcmd"
    mkdir -p "${dst_server_dir}"
    mkdir -p "${dst_conf_basedir}/${dst_conf_dirname}"
    mkdir -p "${data_dir}"
    mkdir -p "${mod_cfg_dir}"
    mkdir -p "${log_save_dir}"
}
# 检查当前系统信息
Check_sys(){
    if [[ -f "/etc/redhat-release" ]]
    then
    release="centos"
    elif cat /etc/issue | grep -q -E -i "debian"
    then
    release="debian"
    elif cat /etc/issue | grep -q -E -i "ubuntu"
    then
    release="ubuntu"
    elif cat /etc/issue | grep -q -E -i "centos|red hat|redhat"
    then
    release="centos"
    elif cat /proc/version | grep -q -E -i "debian"
    then
    release="debian"
    elif cat /proc/version | grep -q -E -i "ubuntu"
    then
    release="ubuntu"
    elif cat /proc/version | grep -q -E -i "centos|red hat|redhat"
    then
    release="centos"
    fi
    if [[ "${release}" != "ubuntu" && "${release}" != "debian" && "${release}" != "centos" ]]
    then
    error "很遗憾！本脚本暂时只支持Debian7+和Ubuntu12+和CentOS7+的系统！" && exit 1
    fi
    bit=`uname -m`
}
# 安装依赖库和必要软件
Install_Dependency(){
    info "安装DST所需依赖库及软件 ..."
    if [[ "${release}" != "centos" ]]
    then
    if [[ "${bit}" = "x86_64" ]]
    then
      sudo dpkg --add-architecture i386
        sudo apt update
        sudo apt install -y lib32gcc1 libstdc++6 libstdc++6:i386 libcurl4-gnutls-dev:i386 tmux wget lua5.2 git openssl libssl-dev curl
    else
      sudo apt update
      sudo apt install -y libstdc++6 libcurl4-gnutls-dev tmux wget lua5.2 git openssl libssl-dev curl
    fi
    else
    if [[ "${bit}" = "x86_64" ]]
    then
      sudo yum install -y tmux glibc.i686 libstdc++ libstdc++.i686 libcurl.i686 wget lua5.2 git openssl openssl-devel curl
    else
      sudo yum install -y wget tmux libstdc++ libcurl lua5.2 git openssl openssl-devel curl
    fi
     fi
}
# Install steamcmd
Install_Steamcmd(){
    if [ ! -f ${DST_HOME}/steamcmd_linux.tar.gz ]
    then
    wget "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" -O "${DST_HOME}/steamcmd_linux.tar.gz"
    fi
    tar -xzvf "${DST_HOME}/steamcmd_linux.tar.gz" -C "${DST_HOME}/steamcmd"
    chmod +x "${DST_HOME}/steamcmd/steamcmd.sh"
}
# Install DST Dedicated Server
Install_Game(){
  user=$(grep '^user' ${data_dir}/userinfo.txt | cut -d '=' -f2) > /dev/null 2>&1
  if [ -z $user ]
  then
    rm ${data_dir}/userinfo.txt
    touch ${data_dir}/userinfo.txt
    echo "user=anonymous" > ${data_dir}/userinfo.txt
    echo "password=" >> ${data_dir}/userinfo.txt
  fi
  user=$(grep '^user' ${data_dir}/userinfo.txt | cut -d '=' -f2)
  password=$(grep '^password' ${data_dir}/userinfo.txt | cut -d '=' -f2)
  Get_game_beta
  if [[ $gamebeta != "" || $gamebeta != "public" ]]
  then
    beta_str="-beta $gamebeta"
  fi
  cd "${DST_HOME}/steamcmd" || exit 1
  ./steamcmd.sh +@ShutdownOnFailedCommand 1 +login ${user} ${password} +force_install_dir "${dst_server_dir}" +app_update "343050" $beta_str validate +quit
  cd ${HOME}
}
# 修复SteamCMD [S_API FAIL] SteamAPI_Init() failed;
Fix_steamcmd(){
  info "修复Steamcmd可能存在的依赖问题 ..."
  mkdir -p "${DST_HOME}/.steam/sdk32"
  cp -v "${DST_HOME}/steamcmd/linux32/steamclient.so" "${DST_HOME}/.steam/sdk32/steamclient.so"
  # fix lib for centos
  if [[ "${release}" == "centos" ]] && [ ! -f "${dst_server_dir}/bin/lib32/libcurl-gnutls.so.4" ]
  then
    info "libcurl-gnutls.so.4 missing ... create a lib link."
    ln -s "/usr/lib/libcurl.so.4" "${dst_server_dir}/bin/lib32/libcurl-gnutls.so.4"
  fi
}
Status_keep(){
    Get_current_cluster
    Get_shard_array
    for shard in $shardarray
    do
    if ! tmux has-session -t DST_"${shard}" > /dev/null 2>&1
    then
      server_alive="false"
      break
    else
      server_alive="true"
    fi
    done
    getsetting "serveropen"
    if [[ $result == "true" &&  "${server_alive}" == "false" ]]
    then
    tip "服务器异常退出，即将重启 ..."
    Reboot_server
    fi
}
Simple_server_status(){
    cluster="无"
    unset server_on
    Get_current_cluster
    Get_shard_array
    for shard in ${shardarray}
    do
    if tmux has-session -t DST_"${shard}" > /dev/null 2>&1
    then
      server_on="${server_on}${shard}"
    fi
    done
    if tmux has-session -t Auto_update > /dev/null 2>&1
    then
    auto_on="开启"
    else
    auto_on="关闭"
    fi
    cluster_name="无"
    if [[ "${server_on}" == "" ]]
    then
    server_on="无"
    fi
    [ -f "${dst_base_dir}/${cluster}/cluster.ini" ] && cluster_name=$(cat "${dst_base_dir}/${cluster}/cluster.ini" | grep "^cluster_name" | cut -d "=" -f2)
    echo -e "\e[33m存档: ${cluster}   开启的世界：${server_on}   名称: ${cluster_name}\e[0m"
    echo -e "\e[33m附加功能进程：${auto_on}\e[0m"
}
Update_MOD(){
    Get_current_cluster
    if [ -f "${dst_base_dir}/${cluster}/${shard}/modoverrides.lua" ]
    then
    Setup_mod
    Download_MOD
    else
    tip "当前存档【${cluster}】没有启用MOD或存档已损坏！"
    fi
}
Download_MOD(){
    info "正在安装/更新新添加的MOD(合集)，请稍候 。。。"
    tip "如长时间卡住在这，请关掉开着的服务器再试，或直接本地上传。"
    if [ ! -d "${dst_base_dir}/downloadmod/Master" ]
    then
    mkdir -p "${dst_base_dir}/downloadmod/Master"
    fi
    if tmux has-session -t DST_MODUPDATE > /dev/null 2>&1
    then
    tmux kill-session -t DST_MODUPDATE
    fi
    cd "${dst_server_dir}/bin" || exit 1
    tmux new-session -s DST_MODUPDATE -d "${dst_bin_cmd} -persistent_storage_root ${dst_conf_basedir} -conf_dir ${dst_conf_dirname} -cluster downloadmod -shard Master"
    sleep 3
    exchangesetting downloadmod_timeouttime 3
    init_downloadmod_timeout_time=$(date +%s)
    while (true)
    do
    if checktime "downloadmod_timeout"
    then
      tip "因网络问题下载MOD超时，请本地上传或重试！。"
      tmux kill-session -t DST_MODUPDATE
      break
    else
      if tmux has-session -t DST_MODUPDATE > /dev/null 2>&1
      then
        if [ $(grep "Your Server Will Not Start" -c "${dst_base_dir}/downloadmod/Master/server_log.txt") -gt 0 ]
        then
          info "MOD安装/更新程序执行完毕完毕，如未更新成功，请直接上传或重试！！"
          tmux kill-session -t DST_MODUPDATE
          break
        fi
      fi
    fi
    init_downloadmod_timeout_time=$(date +%s)
    done
}
Extend_function_setting(){
    while (true)
    do
    clear
    unset parm
    echo -e "\e[33m=====饥荒联机版独立服务器脚本拓展功能设置[Linux-Steam]=====\e[0m"
    echo -e "\e[92m    0. 保存设置重启拓展功能进程并返回主菜单\e[0m"
    echo -e "\e[92m    1. 周期性检查游戏进程是否意外退出，退出自动重启\e[0m"
    echo -e "\e[92m    2. 周期性备份当前开启的存档\e[0m"
    echo -e "\e[92m    3. 周期性检查游戏是否有更新，有则重启更新！[测试版建议开启]\e[0m"
    echo -e "\e[35m涉及时间的设置单位均为分钟，只能输入整数，尽量不要小于五分钟。\e[0m"
    echo -e "\e[33m=====================================================================\e[0m"
    echo -e "\e[92m请输入命令代号：\e[0m\c"
    read efs
    case $efs in
      0)
      Auto_update
      break
      ;;
      1)
      parm="keepalive"
      ;;
      2)
      parm="backupcluster"
      ;;
      3)
      parm="gameupdate"
      ;;
      *)
      error "输入有误！！！"
      ;;
    esac
    efs_menu
    done
}
efs_menu(){
    while (true)
    do
    echo -e "\e[92m请选择设置项： 0.返回上一级  1.是否开启   2.时间周期  ：\e[0m\c"
    read sss
    case $sss in
      0)
      break
      ;;
      1)
      echo -e "\e[92m请选择： 1.开启   2.关闭  ：\e[0m\c"
      read isopen
      case $isopen in
        1)
        st="true"
        exchangesetting "$parm" "$st"
        ;;
        *)
        st="false"
        exchangesetting "$parm" "$st"
        ;;
      esac
      ;;
      2)
      echo -e "\e[92m请输入时间间隔[分钟、整数]：\e[0m\c"
      read dtime
      [[ $dtime == "" ]] && dtime=30
      exchangesetting "${parm}time" "$dtime"
      ;;
      *)
      error "输入有误！！！"
      ;;
    esac
    done
}
checktime(){
    cur_time=$(date +%s)
    getsetting "${1}time"
    [[ $result == "" ]] && result=30
    period=$(($result * 60))
    inittime=`eval echo '$'"init_$1_time"`
    speadtime=$(($cur_time - $inittime))
    if [ $speadtime -gt $period ]
    then
    # 超时
    return 0
    else
    return 1
    fi
}
checkgameupdate(){
    cur_game_version=$(cat "${dst_server_dir}/version.txt")
    Get_game_beta
    if [[ $gamebeta != "" && $gamebeta != "public" ]]
    then
    new_game_version=$(curl -s 'https://forums.kleientertainment.com/game-updates/dst/' | grep 'data-releaseID' | grep -v 'data-currentRelease' | cut -d '/' -f6 | cut -d '-' -f1 | sort -r | head -n 1 | tr -cd '[0-9]')
    else
    new_game_version=$(curl -s 'https://forums.kleientertainment.com/game-updates/dst/' | grep 'data-currentRelease' | cut -d '/' -f6 | cut -d '-' -f1 | sort -r | head -n 1 | tr -cd '[0-9]')
    fi
    if [[ $cur_game_version != "" && $new_game_version != "" && $cur_game_version != $new_game_version ]]
    then
    return 0
    else
    return 1
    fi
}
# 传入MODID
checkmodupdate(){
    unset result
    moddir="workshop-"$1
    Get_installed_mod_version
    cur_mod_ver=$result
    modinfo=$(curl -s "https://wqlin.com/tools/dst.php?type=mod&id=$1")
    unset new_mod_name
    unset new_mod_ver
    if [ $(echo $modinfo | wc -c) -lt 100 ]
    then
    new_mod_name=$(echo $modinfo | cut -d '@' -f1)
    new_mod_ver=$(echo $modinfo | cut -d '@' -f2)
    fi
  if [[ $cur_mod_ver == "uninstalled" && $cur_mod_ver != "" && $new_mod_ver != "" && $cur_mod_ver != $new_mod_ver ]]
    then
    tip "MOD(${new_mod_name}需要更新: ${cur_mod_ver}----->${new_mod_ver})。"
    return 0
    else
    return 1
    fi
}
Getinputlist(){
    inputarray=()
    for i in $1
    do
    if echo $i | grep '-' >/dev/null;
    then
      m=$(echo $i | cut -d '-' -f1)
      n=$(echo $i | cut -d '-' -f2)
      for j in `seq $m $n`
      do
        inputarray[${#inputarray[@]}+1]=$j
      done
    else
      inputarray[${#inputarray[@]}+1]=$i
    fi
    done
}
Get_IP(){
  ip=$(wget -qO- -t1 -T2 ipinfo.io/ip)
  if [[ -z "${ip}" ]]; then
    ip=$(wget -qO- -t1 -T2 api.ip.sb/ip)
    if [[ -z "${ip}" ]]; then
      ip=$(wget -qO- -t1 -T2 members.3322.org/dyndns/getip)
    fi
  fi
}
Post_ipmd5(){
    Get_IP
    send_str=$(echo -n "${ip}" | openssl md5 | cut -d " " -f2)
    curl -s "${my_api_link}/?type=user&ipmd5=${send_str}" > /dev/null 2>&1
    echo "$(date +%s)" > "${data_dir}/ipmd5.txt"
}
# 仅发送md5值做统计，周期内只发送一次，保证流畅性
Send_md5_ip(){
    if [ ! -f "${data_dir}/ipmd5.txt" ]
    then
    Post_ipmd5
    else
    cur_time=$(date +%s)
    old_time=$(cat "${data_dir}/ipmd5.txt")
    cycle=$((${cur_time} - ${old_time}))
    # 周期为七天
    if [ $cycle -gt 604800 ]
    then
      Post_ipmd5
    fi
    fi
}
###
if [[ "$1" == "au" ]]; then
    init_keepalive_time=$(date +%s)
    init_backupcluster_time=$(date +%s)
    init_gameupdate_time=$(date +%s)
    while (true)
    do
    clear
    echo -e "\e[33m=====饥荒联机版独立服务器脚本附加功能进程[Linux-Steam]=====\e[0m"
    info "$(date) [退出请按Ctrl + B松开再按D]"
    getsetting "gameupdate"
    if [[ "$result" == "true" ]]
    then
      if checktime "gameupdate"
      then
        if checkgameupdate
        then
          info "游戏更新($cur_game_version ===> $new_game_version)!"
          Reboot_announce
          Close_server
          Install_Game
          Get_current_cluster
          Get_shard_array
          exchangesetting serveropen true
          Start_shard
        else
          info "游戏无更新！"
        fi
        init_gameupdate_time=$(date +%s)
      fi
      info "游戏自动更新已开启！检查周期 $result 分钟"
    else
      tip "游戏自动更新未开启！"
    fi
    getsetting "keepalive"
    if [[ "$result" == "true" ]]
    then
      if checktime "keepalive"
      then
        Status_keep
        init_keepalive_time=$(date +%s)
      fi
      info "闪退自动重启已开启！检查周期 $result 分钟"
    else
      tip "闪退自动重启未开启！"
    fi
    getsetting "backupcluster"
    if [[ "$result" == "true" ]]
    then
      if checktime "backupcluster"
      then
        Backup_cluster
        init_backupcluster_time=$(date +%s)
      fi
      info "存档自动备份已开启！检查周期 $result 分钟"
    else
      tip "存档自动备份未开启！"
    fi
    info "每五分钟进行一次大循环。。。"
    sleep 300
    done
fi
if [[ "$1" == "sp" ]]; then
    clear
    echo -e "\e[33m=====饥荒联机版独立服务器脚本当前玩家记录后台[Linux-Steam]=====\e[0m"
    Get_single_shard
    tail -f "${dst_base_dir}/${cluster}/${shard}/server_chat_log.txt" | cut -d " " -f2-100
fi
if [[ "$1" == "sa" ]]; then
    while (true)
    do
    clear
    echo -e "\e[33m=====饥荒联机版独立服务器脚本发送公告后台[Linux-Steam]=====\e[0m"
    Get_single_shard
    echo -e "\e[92m请输入你要发送的公告内容，按下回车键发送：\e[0m"
    read an
    tmux send-keys -t DST_"${shard}" "c_announce(\"$an\")" C-m
    info "公告已发送！"
    sleep 1
    done
fi
if [[ "$1" == "ay" ]]; then
    Get_current_cluster
    Analysis_log $2
    exit
fi

# Run from here
Check_sys
First_run_check
Send_md5_ip
clear
Menu
