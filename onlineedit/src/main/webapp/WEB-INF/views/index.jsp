<%--
  Created by IntelliJ IDEA.
  User: zpw
  Date: 15-11-25
  Time: 上午10:22
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ taglib uri="http://www.springframework.org/tags/form" prefix="form" %>
<!DOCTYPE html>
<html>
<head>
	<title>Online Edit</title>
	<script src="/js/jquery-1.11.3.min.js" type="text/javascript"></script>
	<script src="/js/bootstrap.min.js" type="text/javascript"></script>
	<link href="/css/bootstrap.min.css" type="text/css" rel="stylesheet"/>
</head>
<body>
<jsp:include page="inc/nav.jsp"/>
<div class="container-fluid">
	<div class="jumbotron">
		<h1>Online Edit</h1>
		<p>At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
		</p>
		<p><a class="btn btn-primary btn-lg" role="button" href="/admin/index">Enter Admin</a></p>
	</div>
</div>
<jsp:include page="inc/footer.jsp"/>
</body>
</html>
