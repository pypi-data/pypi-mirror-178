### 测试
练习使用psutil获取相关指标并上传包到pypi:
- 内存（memeroy）
- 网络（network）
- 磁盘（disk）
- cpu

### 说明
Monitor类包含cpu()、mem()、net() 、disk()方法分别用于获取cpu、内存、网络及磁盘相关信息。
MyProvider类封装了产生数据的相关方法...
ex:
```python
    # 自定义生成数据元祖/列表
    source_name = ['name', 'email', 'address',
                   'ssn', 'company', 'job',
                   'phone_number', 'email'
                   ]
    provider = MyProvider()
    test_data = provider.function_random(source_name, locale='zh_CN')
    print(test_data)
```  