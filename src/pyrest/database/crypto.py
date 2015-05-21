# encoding: utf-8
# author:   Jan Hybs
import hashlib

salt_prefix = "15646dfs56g"
salt_suffix = "_gsdfg4d6gf"


def password_hash (str):
    return hashlib.sha224 (salt_prefix + str + salt_suffix).hexdigest ()