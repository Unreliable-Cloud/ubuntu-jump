#!/usr/bin/env bash
# reset environment variables that could interfere with normal usage
export GREP_OPTIONS=
# put all utility functions here

# make a temporary file
git_extra_mktemp() {
    mktemp -t "$(basename "$0")".XXXXXXX
}

git_extra_default_branch() {
    local extras_default_branch init_default_branch
    extras_default_branch=$(git config --get git-extras.default-branch)
    init_default_branch=$(git config --get init.defaultBranch)
    if [ -n "$extras_default_branch" ]; then
        echo "$extras_default_branch"
    elif [ -n "$init_default_branch" ]; then
        echo "$init_default_branch"
    else
        echo "main"
    fi
}
#
# check whether current directory is inside a git repository
#

is_git_repo() {
  git rev-parse --show-toplevel > /dev/null 2>&1
  result=$?
  if test $result != 0; then
    >&2 echo 'Not a git repo!'
    exit $result
  fi
}

is_git_repo

: ${GIT_DIR:=$(git rev-parse --git-dir)}

function show_contents {
  local file="${2/#~/$HOME}"
  if [ -f "$file" ]; then
    echo "$1 gitignore: $2" && cat "$file"
  else
    echo "There is no $1 .gitignore yet"
  fi
}

function global_ignore() {
    git config --global core.excludesFile || \
        ([ -n "$XDG_CONFIG_HOME"  ] && echo "$XDG_CONFIG_HOME/git/ignore") || \
        echo "$HOME/.config/git/ignore"
}

function show_global {
  show_contents Global "$(global_ignore)"
}

function add_global {
  local global_gitignore="$(global_ignore)"
  if [ -z "$global_gitignore" ]; then
    echo "Can't find global .gitignore."
    echo ""
    echo "Use 'git config --global --add core.excludesfile ~/.gitignore-global' to set the path to your global gitignore file to '~/.gitignore-global'."
    echo ""
  else
    add_patterns "$global_gitignore" "$@"
  fi
}

function show_local {
  cd "$(git root)"
  show_contents Local .gitignore
}

function add_local {
  cd "$(git root)"
  add_patterns .gitignore "$@"
}

function show_private {
  cd "$(git root)"
  show_contents Private "${GIT_DIR}/info/exclude"
}

function add_private {
  cd "$(git root)"
  test -d "${GIT_DIR}/info" || mkdir -p "${GIT_DIR}/info"
  add_patterns "${GIT_DIR}/info/exclude" "$@"
}

function add_patterns {
  echo "Adding pattern(s) to: $1"
  local file="${1/#~/$HOME}"
  dir_name=$(dirname "$file")
  if [ ! -d "$dir_name" ]; then
      mkdir -p "$dir_name"
  fi
  if [ -s "$file" ]; then
      # If the content of $file doesn't end with a newline, add one
      test "$(tail -c 1 "$file")" != "" && echo "" >> "$file"
  fi
  for pattern in "${@:2}"; do
    echo "... adding '$pattern'"
    (test -f "$file" && test "$pattern" && grep -q -F -x -- "$pattern" "$file") || echo "$pattern" >> "$file"
  done
}

if test $# -eq 0; then
   show_global
   echo "---------------------------------"
   show_local
   echo "---------------------------------"
   show_private
else
  case "$1" in
    -l|--local)
      test $# -gt 1 && add_local "${@:2}" && echo
      show_local
      ;;
    -g|--global)
      test $# -gt 1 && add_global "${@:2}" && echo
      show_global
      ;;
    -p|--private)
      test $# -gt 1 && add_private "${@:2}" && echo
      show_private
      ;;
    *)
      add_local "$@"
      ;;
  esac
fi
