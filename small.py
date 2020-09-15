#usr/bin/env python
#-*- coding:utf-8- -*-


def check_login(func):
    def check(*args, **kwargs):
        print(args)
        print(kwargs)
        return func(*args, **kwargs)

    return check


@check_login
def simple_login(request, kind):
    print("simple test")
    return request


if __name__ == '__main__':
    simple_login("req", "student")