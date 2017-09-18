		var aData = [];

		// 2.步骤二
		// 定义demo函数 (分析接口、数据)
		function demo(data) {
			//var Ul = document.getElementById('ul');
			var html = '';
			aData = [];
			// 如果搜索数据存在 把内容添加进去
			if (data.s.length) {
				// 隐藏掉的ul显示出来
				//Ul.style.display = 'block';
				// 搜索到的数据循环追加到li里
				for (var i = 0; i < data.s.length; i++) {
					//html += '<li>' + data.s[i] + '</li>';<span class="num_right">约100个</span>
					aData.push(data.s[i])
				}
				searchSuggest.dataDisplay(aData);
				// 循环的li写入ul
				//        Ul.innerHTML = html;
			}
		}



	function getQueryString(name) {
var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
var r = window.location.search.substr(1).match(reg);
if (r != null) return unescape(r[2]); return null;
}

	function doSearch(keyword){//搜索动作
	    type=$('input:radio[name="searchType"]:checked').val();
		window.location.assign("searchResult?kw="+encodeURI(keyword)+"&type="+type);
		}
	function doSearchByInput(){//搜索动作
		var keyword=$("#gover_search_key").val();
		//alert(keyword);
		type=$('input:radio[name="searchType"]:checked').val();
		window.location.assign("searchResult?kw="+encodeURI(keyword)+"&type="+type);
		}
		function oSearchSuggest(searchFuc) {
			var input = $('#gover_search_key');
			var suggestWrap = $('#gov_search_suggest');
			var key = "";
			var init = function() {
				input.bind('keyup', sendKeyWord);
				input.bind('blur', function() {
					//console.log('blur');
					setTimeout(hideSuggest, 100);
				}) //这里如果时间太短 会导致li的点击事件无法执行，点击也触发了失去焦点的事件,而且是先执行，，因为点下去就触发了，鼠标抬起来才是click，但此时框已经消失。。。
			}
			var hideSuggest = function() {
				suggestWrap.hide();
			}
			//发送请求，根据关键字到后台查询
			var sendKeyWord = function(event) {

                if (event.keyCode == 13){
                doSearchByInput();
                }
				//键盘选择下拉项
			    if (suggestWrap.css('display') == 'block'
						&& event.keyCode == 38 || event.keyCode == 40) {//上下按钮
					var current = suggestWrap.find('li.hover');
					if (event.keyCode == 38) {
						if (current.length > 0) {
							var prevLi = current.removeClass('hover').prev();
							if (prevLi.length > 0) {
								prevLi.addClass('hover');
								input.val(prevLi.html());
							}
						} else {
							var last = suggestWrap.find('li:last');
							last.addClass('hover');
							input.val(last.html());
						}
					} else if (event.keyCode == 40) {
						if (current.length > 0) {
							var nextLi = current.removeClass('hover').next();
							if (nextLi.length > 0) {
								nextLi.addClass('hover');
								input.val(nextLi.html());
							}
						} else {
							var first = suggestWrap.find('li:first');
							first.addClass('hover');
							input.val(first.html());
						}
					}
					//输入字符
				} else {
					var valText = $.trim(input.val());
					if (valText == '' || valText == key) {
						return;
					}
					searchFuc(valText);
					key = valText;
				}
			}
			//请求返回后，执行数据展示
			this.dataDisplay = function(data) {
				if (data.length <= 0) {
					suggestWrap.hide();
					return;
				}
				//往搜索框下拉建议显示栏中添加条目并显示
				var li;
				var tmpFrag = document.createDocumentFragment();
				suggestWrap.find('ul').html('');
				for (var i = 0; i < data.length; i++) {
					li = document.createElement('li');
					li.innerHTML = data[i];
					tmpFrag.appendChild(li);
				}
				suggestWrap.find('ul').append(tmpFrag);
				suggestWrap.show();
				//suggestWrap = $('#gov_search_suggest');

				//为下拉选项绑定鼠标事件
				suggestWrap.find('li').on('mousedown', function() {//原来是click，但是会弱后于blur事件导致选择框消失，so
					//alert('click');
					//$(this).find("span").remove();
					input.val(this.innerHTML);
					doSearch(this.innerHTML);
					suggestWrap.hide();
				}).hover(function() {
					suggestWrap.find('li').removeClass('hover');
					$(this).addClass('hover');
				}, function() {
					$(this).removeClass('hover');
				});
			}
			init();
		};
		//实例化输入提示的JS,参数为进行查询操作时要调用的函数名
		var searchSuggest = new oSearchSuggest(sendKeyWordToBack);
		//这是一个模似函数，实现向后台发送ajax查询请求，并返回一个查询结果数据，传递给前台的JS,再由前台JS来展示数据。本函数由程序员进行修改实现查询的请求
		//参数为一个字符串，是搜索输入框中当前的内容
		function sendKeyWordToBack(keyword) {
			var script = document.createElement('script');
			//给定要跨域的地址 赋值给src
			script.src = 'https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd='
					+encodeURI(keyword) + '&cb=demo';//这里是要请求的跨域的地址 我写的是百度搜索的跨域地址

			// 将组合好的带src的script标签追加到body里 //这样应该就会在接下来执行了？这地方很奇怪，貌似是新增的js才会执行，这里没删除js
			document.body.appendChild(script);//感觉应该是对象丢失了  应该需要重新绑定一把？
			//将返回的数据传递给实现搜索输入框的输入提示js类

		}

