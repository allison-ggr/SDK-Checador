<?php

$cad="";
for($i=0;$i<strlen($decrypt);$i++){
    if($i==0){
        $cad.='{"horario'.$i+1;
    }
    else{
        
        if(substr($decrypt,$i,1)=='&'){
            $cad.='","';
        }
        if(substr($decrypt,$i,1)=='='){
            $cad.='":"';
        }
        if(substr($decrypt,$i,1)=='-'){
            $cad.='=';
        }
        if(substr($decrypt,$i,1)!='&' && substr($decrypt,$i,1)!='=' && substr($decrypt,$i,1)!='-'){
            $cad.=substr($decrypt,$i,1);
        }
        
    }
}
$cad=$cad.'"}';

?>