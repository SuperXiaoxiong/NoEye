<?php 
//����һ�����ݿ���Ϣ��ѯҳ�棬ֱ�Ӳ�ѯ���ݿ���Ϣ������
//�����Ҫ���Ӱ�ȫ�ԣ�����ʹ��.htaccess�Ը�php�ķ���������
//TODO ��ʱ������Ҫ��չ����pythonдһ��ҳ��


error_reporting(E_ERROR);
$g_link = false;

function GetMyConnection()
{
    global $g_link;
    if( $g_link )
        return $g_link;
    $g_link = mysql_connect( 'localhost', 'root', 'root') or die('Could not connect to server.' );
    mysql_select_db('noeye', $g_link) or die('Could not select database.');
    return $g_link;
}

function CleanUpDB()
{
    global $g_link;
    if( $g_link != false )
        mysql_close($g_link);
    $g_link = false;
}

 
  function Query(){
    $con=GetMyConnection();
    $query = sprintf("SELECT prefixdata, lastaccess FROM dns_query");
     
     // Perform Query
    $result = mysql_query($query,$con);
    while ($row = mysql_fetch_assoc($result)) {
             echo htmlentities($row['prefixdata'], ENT_QUOTES)."<------->";             
             echo $row['lastaccess']."<br/>"; ;        
    }
     
    $query = sprintf("SELECT queried_key, lastaccess FROM url_query");
      
     // Perform Query
    $result = mysql_query($query,$con);
    while ($row = mysql_fetch_assoc($result)) {
         echo htmlentities($row['queried_key'], ENT_QUOTES)."<------->";
         echo $row['lastaccess']."<br/>"; ;
    }
      
    
    CleanUpDB();   
 }
Query();


?>