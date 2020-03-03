# some aliases
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias grep='grep --color=auto'
alias l='ls -CF'
alias la='ls -A'
alias ll='ls -alF'
alias ls='ls --color=auto'

# .bashrc is not sourced when you log in using SSH. You need to source it in your .bash_profile like this:
if [ -f ~/.bashrc ]; then
  . ~/.bashrc
fi
