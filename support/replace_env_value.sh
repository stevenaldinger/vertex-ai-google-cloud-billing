#!/usr/bin/env bash

# usage: replace_env_value.sh <env_var_name> <env_var_value> <env_file_path>

env_var_name=$1
env_var_value=$2
env_file_path=$3

echo "Replacing $env_var_name with $env_var_value in $env_file_path"

if [ -z "$env_var_name" ]; then
  echo "env_var_name is required"
  exit 1
fi

if [ -z "$env_var_value" ]; then
  echo "env_var_value is required"
  exit 1
fi

if [ -z "$env_file_path" ]; then
  echo "env_file_path is required"
  exit 1
fi

# if the env var is already set, replace it
if grep -q $env_var_name $env_file_path; then
  # can't use inline "sed -i" on MacOS because of VirtioFS
  # https://forums.docker.com/t/sed-couldnt-open-temporary-file-xyz-permission-denied-when-using-virtiofs/125473
  sed "s;${env_var_name}=.*;${env_var_name}=${env_var_value};g" $env_file_path > $env_file_path.tmp
  
  mv -f $env_file_path.tmp $env_file_path
else
  # otherwise, add it to the end of the file
  echo "$env_var_name=$env_var_value" >> $env_file_path
fi
