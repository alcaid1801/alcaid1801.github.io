import numpy as np

## 随机生成两个班级
red = np.random.randn( 10000, 1 ) * 5 + 80;
red[red > 100] = 100;

blue = np.random.randn( 10000, 1 ) * 15 + 70;
blue[blue > 100] = 100;

## 展现成绩分布
figure()
hist( red, arange(100), normed=True, alpha=0.5, color='r', label='Red' );
hist( blue, arange(100), normed=True, alpha=0.5, color='b', label='Blue' );
xlabel('Score')
xlim( 0, 100 );
legend()


## 计算两个班的平均分和标准差
stats = array( [ [ np.average(red), np.std(red) ], [ np.average(blue), np.std(blue) ] ] )

print '红班 | %0.2f | %0.2f'%(stats[0,0],stats[0,1])
print '蓝班 | %0.2f | %0.2f'%(stats[1,0],stats[1,1])


## 减去平均分操作
red_avg = red - np.average(red);
blue_avg = blue - np.average(blue);

## 展现
figure()
hist( red_avg, arange(-50,50), normed=True, alpha=0.5, color='r', label='Red' );
hist( blue_avg, arange(-50,50), normed=True, alpha=0.5, color='b', label='Blue' );
xlabel('Score')
xlim( -50, 50 );
legend()


## 除以标准差
red_std = red_avg/np.std(red);
blue_std = blue_avg/np.std(blue);

## 展现
figure()
hist( red_std, arange(-5,5,0.1), normed=True, alpha=0.5, color='r', label='Red' );
hist( blue_std, arange(-5,5,0.1), normed=True, alpha=0.5, color='b', label='Blue' );
xlabel('Score')
xlim( -5, 5 );
legend()


## 投影到500分平均分, 100分标准差的数据上
red_renorm = red_std * 100 + 500;
blue_renorm = blue_std * 100 + 500;

## 展现
figure()
hist( red_renorm, arange(100,800,10), normed=True, alpha=0.5, color='r', label='Red' );
hist( blue_renorm, arange(100,800,10), normed=True, alpha=0.5, color='b', label='Blue' );
xlabel('Score')
xlim( 0, 800 );
legend()



