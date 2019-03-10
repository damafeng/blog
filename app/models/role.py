from . import Model
"""
用户权限功能，为每个用户赋予角色，每个角色可配置相应权限
关注  0x01
评论  0x02   
发帖  0x04
管理评论    0x08
管理员权限   0x80

Role字段
name :  Stranger(0x00)  NormalUser(0x07)    Admin(0x88)
permissions:
default: 新注册用户给赋值哪种Role属性
"""


class Role(Model):
    __fields__ = Model.__fields__ + [
        ('name', str, ''),
        ('permission', int, 0),
        ('default', bool, False),
    ]

    # 添加配置Role
    @classmethod
    def insert_roles(cls):
        roles = [{
                'name': 'User',
                'permission': Permission.FOLLOW | Permission.COMMENT | Permission.WRITE,
                'default': True,
            },
            {
                'name': 'Administrator',
                'permission': 0xff,
                'default': False,
            }
        ]
        for r in roles:
            query_form = {
                'name': r['name'],
            }
            cls.upsert(query_form, r)


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80
