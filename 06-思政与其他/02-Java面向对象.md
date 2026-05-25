# 02-Java面向对象

## 一、项目概述

《面向对象程序设计（Java）》期末考核项目，包含两个Java程序的设计与实现。

## 二、项目要求

### 项目结构
每个项目需包含：
1. **功能说明**：描述程序的功能和用途
2. **代码**：完整的Java源代码
3. **输出效果图**：程序运行结果截图
4. **结果分析**：对运行结果的分析和说明

### 参考题目
- **项目1**：如广东工商饭堂点菜计价程序
- **项目2**：如个人主页等程序

## 三、Java面向对象核心知识

### 面向对象三大特性

#### 1. 封装（Encapsulation）
```java
public class Student {
    private String name;    // 私有属性
    private int age;

    // 公有方法访问私有属性
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public int getAge() { return age; }
    public void setAge(int age) {
        if (age > 0 && age < 150) {
            this.age = age;
        }
    }
}
```

#### 2. 继承（Inheritance）
```java
public class Animal {
    protected String name;
    public void eat() { System.out.println(name + "在吃东西"); }
}

public class Dog extends Animal {
    public void bark() { System.out.println(name + "在叫"); }
    // Dog继承了Animal的eat()方法和name属性
}
```

#### 3. 多态（Polymorphism）
```java
public class Animal {
    public void sound() { System.out.println("动物叫"); }
}

public class Cat extends Animal {
    @Override
    public void sound() { System.out.println("喵喵喵"); }
}

public class Dog extends Animal {
    @Override
    public void sound() { System.out.println("汪汪汪"); }
}

// 多态使用
Animal animal = new Cat();  // 父类引用指向子类对象
animal.sound();  // 输出"喵喵喵"
```

### 类与对象
```java
// 类的定义
public class MenuItem {
    private String name;
    private double price;

    // 构造方法
    public MenuItem(String name, double price) {
        this.name = name;
        this.price = price;
    }

    // 方法
    public double getPrice() { return price; }
    public String toString() { return name + ": ¥" + price; }
}

// 创建对象
MenuItem item = new MenuItem("宫保鸡丁", 28.0);
```

### 接口
```java
public interface Payable {
    double calculateTotal();
    void printReceipt();
}

public class Order implements Payable {
    private List<MenuItem> items = new ArrayList<>();

    @Override
    public double calculateTotal() {
        return items.stream().mapToDouble(MenuItem::getPrice).sum();
    }

    @Override
    public void printReceipt() {
        System.out.println("=== 账单 ===");
        items.forEach(System.out::println);
        System.out.println("总计: ¥" + calculateTotal());
    }
}
```

### 异常处理
```java
try {
    // 可能抛出异常的代码
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("算术异常: " + e.getMessage());
} finally {
    // 无论是否异常都会执行
    System.out.println("执行完毕");
}
```

### 集合框架
```java
import java.util.*;

// ArrayList - 动态数组
List<String> list = new ArrayList<>();
list.add("元素1");
list.get(0);

// HashMap - 键值对
Map<String, Double> menu = new HashMap<>();
menu.put("宫保鸡丁", 28.0);
menu.get("宫保鸡丁");

// 遍历
for (Map.Entry<String, Double> entry : menu.entrySet()) {
    System.out.println(entry.getKey() + ": ¥" + entry.getValue());
}
```

## 四、项目报告模板

```markdown
# 期末考核项目报告

## 1. 第一题XX程序
### 1.1 功能说明
描述程序功能...

### 1.2 代码
（粘贴完整代码）

### 1.3 输出效果图
（粘贴运行截图）

### 1.4 结果分析
分析运行结果...

## 2. 第二题XX程序
### 2.1 功能说明
### 2.2 代码
### 2.3 输出效果图
### 2.4 结果分析

## 3. 项目总结
总结学习收获和改进方向...
```

## 五、评分要点

| 项目 | 分值 | 要求 |
|------|------|------|
| 功能说明 | 10% | 清晰描述程序功能 |
| 代码质量 | 40% | 代码规范、结构清晰、无bug |
| 输出效果 | 20% | 运行结果正确、截图清晰 |
| 结果分析 | 20% | 分析有深度、逻辑清晰 |
| 项目总结 | 10% | 总结学习收获 |
