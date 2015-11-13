from django.conf.urls import patterns, include, url

urlpatterns = patterns('djforms.jobpost.views',
    url(
        r'^success', view = 'data_entered', name = 'data_entered'
    ),
    url(
        r'^createpost/$', view = 'post_create', name = 'post_create'
    ),
    url(
        r'^user-post-list/(?P<page>\w)/$',
        view = 'user_post_list', name  = 'user_post_list_paginated'
    ),
    url(
        r'^user-post-list/$', view = 'user_post_list', name = 'user_post_list'
    ),
    url(
        r'^post-manage-list/(?P<page>\w)/$',
        view = 'post_manage_list', name = 'post_manage_list_paginated'
    ),
    url(
        r'^post-manage-list/$',
        view = 'post_manage_list', name = 'post_manage_list'
    ),
    url(
        r'^managepost/(?P<pid>\d+)/$',
        view = 'post_manage', name = 'post_manage'
    ),
    url(
        r'^departments/(?P<slug>[-\w]+)/$',
        view = 'department_detail', name = 'department_detail'
    ),
    url(
        r'^departments/page/(?P<page>\w)/$',
        view = 'department_list', name = 'department_list_paginated'
    ),
    url(
        r'^departments/$', view = 'department_list', name = 'department_list'
    ),
    url(
        r'^applicants/delete/$',
        view = 'applicants_delete', name = 'applicants_delete'
    ),
    url(
        r'^search/$', view = 'search', name    = 'post_search'
    ),
    url(
        r'^page/(?P<page>\w)/$',
        view = 'post_list', name = 'post_index_paginated'
    ),
    url(
        r'^$', view = 'post_list', name = 'post_index'
    ),
    url(
        r'^(?P<pid>\d+)/$',
        view = 'post_detail', name = 'post_detail'
    )
)
