## About license
BSD开源协议是一个给于使用者很大自由的协议。可以自由的使用，修改源代码，也可以将修改后的代码作为开源或者专有软件再发布。 当你发布使用了BSD协议的代码，或则以BSD协议代码为基础做二次开发自己的产品时，需要满足三个条件：
1． 如果再发布的产品中包含源代码，则在源代码中必须带有原来代码中的BSD协议。
2． 如果再发布的只是二进制类库/软件，则需要在类库/软件的文档和版权声明中包含原来代码中的BSD协议。
3． 不可以用开源代码的作者/机构名字和原来产品的名字做市场推广。
BSD代码鼓励代码共享，但需要尊重代码作者的著作权。BSD由于允许使用者修改和重新发布代码，也允许使用或在BSD代码上开发商业软件发布和销售，因此是对商业集成很友好的协议。而很多的公司企业在选用开源产品的时候都首选BSD协议，因为可以完全控制这些第三方的代码，在必要的时候可以修改或者二次开发。

## How to use it?

* Dependency
base58.py
blocktools.py
block.py

* Data Pipline
```
spark-submit spark_parser.py local[*] filepath1 filepath ...
spark-submit spark_mapinput.py local[*]
spark-submit sprk_mapaddr.py local[*]
```



## Block Chain Tools

Block chain parser implementation written in python. Contains examples for Bitcoin and Litecoin.

blocktools.py - tools for reading binary data from block files
block.py - classes for Blocks, Transactions
parser.py - Genesis block demo
sight.py - block parser
5megBlock.dat - first 5 megs from blk00000.dat
blk65.dat - first 5 megs from blk00065.dat

## Usage

'python sight.py 1M.dat'

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Credits

Alex Gorale

## License

BSD 3

