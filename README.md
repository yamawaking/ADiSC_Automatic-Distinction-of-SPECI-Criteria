# ADiSC
ADiSC- Automatic Distinction of SPECI Criteria

ADiSC（アディスク）……飛行場実況気象報特別観測基準自動判別ツール
## Overview
-ADiSC is a Python tool to detect and identify if weather changes meet SPECI criteria for aviation weather observations. 

  アディスクは、航空気象観測において、天気変化が飛行場実況気象報特別観測基準に該当するか否かを自動的に判別するPythonツールです。
  
-The SPECI criteria varies depending on airport. So ADiSC employs a method where users set criteria, and the system determines whether or not SPECI is necessary based on those criteria.

  特別観測基準は飛行場により異なります。そのため、ADiSCは、ユーザーが観測基準を設定し、それに従って特別観測が必要か否かを決定するシステムを採用しています。
  
-This tool may be useful for beginners and teachers of aviation weather observation and also may be able to contribute to automating it.
  
  このツールは、航空気象観測の初学者や指導者にとって有益である可能性があります。また、その自動化にも資することが期待できます。
  
## How to use
1. Set the SPECI criteria of your observatory in CONFIG.

    特別観測基準をCONFIG欄にて入力してください。

  You can select and set them in detail like "send SPECI if wind direction changed by 60 degree when previous wind speed or current wind speed is more than 10KT" or "send SPECI when it deteriorates but do not send it when it improves".
  
  CONFIG欄では、特別観測基準を細かく設定することができます。「風速が10KT以上のときに風向が60度変化した場合、特別観測を送信する」「天気が悪化した場合は特別観測を送信するが、好転の場合は送信しない」など。

2. Imput the latest and current observation values.
 
   最近の観測値と現在の観測値を入力してください。
 
  Here are a few points to note
  
  いくつか使用上の注意点があります。
  
    1. For wind direction, if it is VRB or the wind condition is CALM, input "VRB", not 0.
    
       風向について、VRB（不定）またはCALM（静穏）の場合は0等ではなく"VRB"と入力してください。
    
    2. For "previous_weather", "current_weather", "previous_ceil" and "current_ceil", if they are not exist, input "" (2 double quotation marks), not 0 or "None". 
    
       現在天気とシーリングについては、存在していない場合は0やNoneではなく"" (ダブルクォーテーションマーク2つ) を入力してください。
   
     3. For "previous_weather" and "current_weather", you must input the same phenomenon in the same frame. For example, if you input "-RA" in the frame "previous_weather1" and it chaged into "RA", input it in the frame "current_weather1" not in "current_weather2"-"current_weather4". If you input them in different frame, the distinction of intensity change will not be done correctly.
   
      現在天気については、同一の現象は同一の枠へ入力してください。たとえば、"previous_weather1"に"-RA"を入力し、それが"RA"へ変わったとすれば、"current_weather2"～"current_weather4"の枠ではなく、"current_weather1"に"RA"と入力してください。枠が異なると、強度変化の判定が正しく行われません。
   
    3. Run module.

         実行してください。
   
      Make sure to check the result again by yourself whether or not it is correct.

      実行結果が正しいかどうか、必ず自ら再確認をおこなってください。

## Postscript
The available-on-the-web version of this tool is under construction now. It will become much easier to use.

このツールのウェブ上で使用可能なバージョンを開発中です。より簡単に操作できるようになるでしょう。