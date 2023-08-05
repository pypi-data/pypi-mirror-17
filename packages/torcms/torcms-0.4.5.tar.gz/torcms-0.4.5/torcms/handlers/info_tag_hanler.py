# -*- coding:utf-8 -*-

import json

import tornado.web
import config
from torcms.model.inforcatalog_model import MInforCatalog
from torcms.model.infor_model import MInfor as  MInfor
from torcms.core.base_handler import BaseHandler

from torcms.core.torcms_redis import redisvr


class InfoTagHandler(BaseHandler):
    def initialize(self, hinfo=''):
        self.init()
        self.template_dir_name = 'infor'
        self.minfo = MInfor()
        self.mcat = MInforCatalog

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 1:
            self.list(url_str)
        elif len(url_arr) == 2:
            if url_arr[0] == 'remove':
                self.remove_redis_keyword(url_arr[1])
            else:
                self.list(url_arr[0], url_arr[1])

    @tornado.web.authenticated
    def remove_redis_keyword(self, kw):
        redisvr.srem(config.redis_kw + self.userinfo.user_name, kw)
        return json.dump({}, self)

    def list(self, tag_slug, cur_p=''):

        if self.get_current_user():
            redisvr.sadd(config.redis_kw + self.userinfo.user_name, tag_slug)

        if cur_p == '':
            current_page_num = 1
        else:
            current_page_num = int(cur_p)

        tag_name = 'fd'
        kwd = {
            'tag_name': tag_name,
            'tag_slug': tag_slug,
            'title': tag_name,
        }

        info = self.minfo.query_by_tagname(tag_slug)

        page_num = int(info.count() / config.page_num) + 1

        self.render('{0}/label/list.html'.format(self.template_dir_name),
                    kwd=kwd,
                    userinfo=self.userinfo,
                    infos=self.minfo.get_label_fenye(tag_slug, current_page_num),
                    pager=self.gen_pager(tag_slug, page_num, current_page_num),

                    )

    def gen_pager(self, cat_slug, page_num, current):
        '''
        cat_slug 分类
        page_num 页面总数
        current 当前页面
        '''

        if page_num == 1:
            return ''

        pager_shouye = '''
        <li class="{0}">
        <a  href="/info_tag/{1}">&lt;&lt; 首页</a>
                    </li>'''.format('' if current <= 1 else '', cat_slug)

        pager_pre = '''
                    <li class=" previous {0}">
                    <a  href="/info_tag/{1}/{2}">&lt; 前页</a>
                    </li>
                    '''.format('' if current <= 1 else '', cat_slug, current - 1)
        pager_mid = ''
        for ind in range(0, page_num):
            tmp_mid = '''
                    <li class=" page {0}">
                    <a  href="/info_tag/{1}/{2}">{2}</a></li>
                    '''.format('active' if ind + 1 == current else '', cat_slug, ind + 1)
            pager_mid += tmp_mid
        pager_next = '''
                    <li class=" next {0}">
                    <a  href="/info_tag/{1}/{2}">后页 &gt;</a>
                    </li>
                    '''.format('' if current >= page_num else '', cat_slug, current + 1)
        pager_last = '''
                    <li class=" last {0}">
                    <a href="/info_tag/{1}/{2}">末页
                        &gt;&gt;</a>
                    </li>
                    '''.format('' if current >= page_num else '', cat_slug, page_num)
        pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
        return (pager)
