<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags"%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions"%>
<!DOCTYPE html>
<html>
<head>
<title>${i18n['app.title']}${site.title}${_title}</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="pragma" content="no-cache">
<meta http-equiv="cache-control" content="no-cache">
<meta http-equiv="expires" content="0">
<link rel="shortcut icon" href="${static_dir}/images/favicon.ico"
	type="image/x-icon" />
<link rel="icon" href="${static_dir}/images/favicon.ico"
	type="image/x-icon" />
<style>
html {
	overflow: hidden;
	height: 100%
}

.localedit {
	position: absolute;
	top: 5px;
	left: 100px;
	filter: alpha(opacity : 100);
	opacity: 1;
	z-index: 3;
	font-size: 9pt;
	font-family: 'Microsoft YaHei UI', 'Microsoft YaHei', 微软雅黑, SimSun, 宋体,
		sans-serif;
}

.titleName {
	position: absolute;
	top: 3px;
	left: 200px;
	right: 200px;
	text-align: center;
	filter: alpha(opacity : 100);
	opacity: 1;
	z-index: 2;
	font-family: 'Microsoft YaHei UI', 'Microsoft YaHei', 微软雅黑, SimSun, 宋体,
		sans-serif;
}
</style>

</head>
<body style="height: 100%; margin: 0;">

	<c:set var="supportLabel"
		value=" 【<font color='#5c6e7e'>仅支持Office2010及以上版本</font>】"></c:set>
	<c:set var="protocalOff" value="ms-word"></c:set>
	<c:if test="${ suffix == 'docx' }">
		<div class="localedit">
			<span style="vertical-align: middle;"> <img
				src="${base_dir }/images/ms-word.png"
				style="padding-right: 2px; margin-bottom: -3px" /></span> <a
				style="text-decoration: none; color: #444444;"
				href="${protocalOff}:ofe|u|${local}" target="blank">本地Word协同编辑${supportLabel}</a>
		</div>
	</c:if>
	<!--  
	<c:if test="${ suffix == 'xlsx' }">
		<c:set var="protocalOff" value="ms-excel"></c:set>
		<div class="localedit">
			<span style="vertical-align: middle;"> <img
				src="${base_dir }/images/ms-excel.png"
				style="padding-right: 2px; margin-bottom: -3px" /></span> <a
				style="text-decoration: none; color: #444444;"
				href="${protocalOff}:ofe|u|${local}" target="blank">本地EXCEL协同编辑${supportLabel}</a>
		</div>
	</c:if>
	-->
	<c:if test="${ suffix == 'pptx' }">
		<c:set var="protocalOff" value="ms-powerpoint"></c:set>
		<div class="localedit">
			<span style="vertical-align: middle;"> <img
				src="${base_dir }/images/ms-powerpoint.png"
				style="padding-right: 2px; margin-bottom: -3px" /></span> <a
				style="text-decoration: none; color: #444444;"
				href="${protocalOff}:ofe|u|${local}" target="blank">本地PowerPoint协同编辑${supportLabel}</a>
		</div>
	</c:if>

<!--  
	<div class="titleName">${docName}</div>
-->
	<div id="previewIframe"
		style="width: 100%; border: 0; height: 100%; position: fixed; bottom: 0; top: 0; z-index: 1;">
		<iframe name="iframe" id="iframe"
			style="width: 100%; border: 0; height: 100%" src="${online}"></iframe>
	</div>
	<script>
		(function() {
			document.getElementById("iframe").height = document.body.clientHeight;
			window.onresize = function() {
				document.getElementById("iframe").height = document.body.clientHeight;
			};
		})();
	</script>

</body>
</html>


