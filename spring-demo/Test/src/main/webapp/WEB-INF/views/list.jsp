<%--
  Created by IntelliJ IDEA.
  User: zhangpan05
  Date: 2016/1/5
  Time: 22:46
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<c:set var="ctx" value="${pageContext.request.contextPath}"/>

<html>
<head>
    <title>Product list</title>
</head>
<body>
<h2>list</h2>
<table>
    <tr>
        <th>Id</th><th>name</th><th>price</th><th>option</th>
    </tr>
<c:forEach var="product" items="${products}">
    <tr>
        <td>${product.id}</td>
        <td>${product.name}</td>
        <td>${product.price}</td>
        <td>
            <a href="${ctx}/product/edit/${product.id}">edit</a>
            <a href="${ctx}/product/del/${product.id}">delete</a>
        </td>
    </tr>
</c:forEach>
</table>
<a href="${ctx}/product/add">add product</a>
</body>
</html>
