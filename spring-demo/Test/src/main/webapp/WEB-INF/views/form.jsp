<%--
  Created by IntelliJ IDEA.
  User: zhangpan05
  Date: 2016/1/6
  Time: 0:15
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://www.springframework.org/tags/form" prefix="form" %>

<c:set var="ctx" value="${pageContext.request.contextPath}"/>

<html>
<head>
    <title>Title</title>
</head>
<body>
<form:form action="${ctx}/product/update" method="post" modelAttribute="product">
    <form:label path="id">Id</form:label>
    <form:input path="id"></form:input>
    <form:label path="name">name</form:label>
    <form:input path="name"></form:input>
    <form:label path="price">price</form:label>
    <form:input path="price"></form:input>
    <input type="submit"/>
</form:form>
</body>
</html>
