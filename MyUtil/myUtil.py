
from django.core.paginator import Paginator


def pageUtil(page,pagecount,objlist):
    paginator = Paginator(objlist, pagecount)
    page_num = paginator.num_pages
    page_sell_list = paginator.page(page)
    if page_sell_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_sell_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page
    context = {
        'oblist': page_sell_list.object_list,
        'curr_page': page,
        'previous_page': previous_page,
        'next_page': next_page,
        'total_page': page_num,
        'total_count': len(objlist),
    }
    return context