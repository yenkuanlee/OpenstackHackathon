scale out       
        $ python control.py $user $passwd $ip


scale in        
        $ python ScaleIn.py $ip


insert (插入$number筆假資料)    
        $ python influx.py $number (Insert by master)           
        $ python MultiInsert.py $number (Insert by each nodes)


(1) crontab 定期執行inert               
(2) nohup python test &> nohup &        # 無窮迴圈每秒差入
