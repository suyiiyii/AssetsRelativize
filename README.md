# AssetsRelativize

一个可以将md/tex文件中的绝对路径转换成相对路径的小工具


## 行为

1. 将文件备份一份，以.bak后缀保存到同一目录下
2. 读取文档中的图片路径
3. 将图片复制到当前目录下的 assets 文件夹下
4. 更新文档中的图片路径
5. 保存文档

## 已知问题

文件名不能重名，不然复制到同一目录下会覆盖，目前检测到目标路径有文件会抛出异常
