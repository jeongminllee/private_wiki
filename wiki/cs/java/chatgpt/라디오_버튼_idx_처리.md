---
type: Concept
title: "라디오 버튼 idx 처리"
description: "CS - Java 프로그래밍 - ChatGPT 대화 추출 노트 (2026-05-26)"
tags: [cs, chatgpt-export]
timestamp: 2026-05-26
status: active
---

# 라디오 버튼 idx 처리

> **카테고리**: `CS - Java 프로그래밍`  
> **원천**: ChatGPT 대화 아카이브 (`raw/notes/Chatgpt_2026-08-02-23-14-23`)  
> **작성일**: 2026-05-26

## 💬 대화 내용 및 Q&A

### 💡 답변 (Assistant)
좋아요. 이 코드는 **라디오 버튼마다 “자기 번호(idx)”를 기억하게 만들고 싶은 상황**입니다.

핵심은 `for`문 안에서 `i` 값을 바로 익명 클래스 안에서 쓰면 안 되고, **반복마다 고정된 값으로 복사한 변수**를 만들어야 합니다.

## 수정 코드

```java
for (int i = 0; i < radio.length; i++) {
    radio[i] = new JRadioButton(text[i]);
    g.add(radio[i]);
    radioPanel.add(radio[i]);

    final int idx = i;   // 현재 i 값을 idx에 고정

    radio[i].addItemListener(new ItemListener() {
        @Override
        public void itemStateChanged(ItemEvent e) {
            if (e.getStateChange() == ItemEvent.SELECTED) {
                imageLabel.setIcon(images[idx]);
            }
        }
    });
}
```

전체 코드에서 이 부분만 바꾸면 됩니다.

---

## 왜 `final int idx = i;`가 필요한가?

`for`문의 `i`는 계속 바뀝니다.

```java
i = 0
i = 1
i = 2
```

그런데 `ItemListener`는 버튼을 만들 때 바로 실행되는 게 아니라, **나중에 사용자가 클릭했을 때 실행**됩니다.

그래서 Java는 익명 클래스 내부에서 바깥 변수 `i`를 직접 쓰는 것을 제한합니다.

예를 들어 이렇게 하면 안 됩니다.

```java
radio[i].addItemListener(new ItemListener() {
    @Override
    public void itemStateChanged(ItemEvent e) {
        imageLabel.setIcon(images[i]); // 오류 발생
    }
});
```

왜냐하면 `i`는 반복문이 돌면서 계속 변하는 변수이기 때문입니다.

그래서 반복 한 번마다 현재 값을 따로 저장합니다.

```java
final int idx = i;
```

그러면 각각의 버튼은 자기 번호를 기억합니다.

```java
사과 버튼  -> idx = 0
배 버튼    -> idx = 1
체리 버튼  -> idx = 2
```

---

## 네 코드에 적용한 전체 예시

```java
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;

import javax.swing.ButtonGroup;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.SwingConstants;

public class Swing0526_8 extends JFrame {
    private JRadioButton[] radio = new JRadioButton[3];
    private String[] text = {"사과", "배", "체리"};

    private ImageIcon[] images = {
            new ImageIcon("images/apple.jpg"),
            new ImageIcon("images/pear.jpg"),
            new ImageIcon("images/cherry.jpg")
    };

    private JLabel imageLabel = new JLabel();

    public Swing0526_8() {
        setTitle("라디오 버튼 Item Event 예제");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        Container c = getContentPane();
        c.setLayout(new BorderLayout());

        JPanel radioPanel = new JPanel();
        radioPanel.setBackground(Color.GRAY);

        ButtonGroup g = new ButtonGroup();

        for (int i = 0; i < radio.length; i++) {
            radio[i] = new JRadioButton(text[i]);
            g.add(radio[i]);
            radioPanel.add(radio[i]);

            final int idx = i;

            radio[i].addItemListener(new ItemListener() {
                @Override
                public void itemStateChanged(ItemEvent e) {
                    if (e.getStateChange() == ItemEvent.SELECTED) {
                        imageLabel.setIcon(images[idx]);
                    }
                }
            });
        }

        radio[2].setSelected(true);

        c.add(radioPanel, BorderLayout.NORTH);
        c.add(imageLabel, BorderLayout.CENTER);

        imageLabel.setHorizontalAlignment(SwingConstants.CENTER);

        setSize(250, 200);
        setVisible(true);
    }

    public static void main(String[] args) {
        new Swing0526_8();
    }
}
```

---

## 더 짧게 람다식으로 쓰면

Java 8 이상이면 이렇게도 가능합니다.

```java
for (int i = 0; i < radio.length; i++) {
    radio[i] = new JRadioButton(text[i]);
    g.add(radio[i]);
    radioPanel.add(radio[i]);

    final int idx = i;

    radio[i].addItemListener(e -> {
        if (e.getStateChange() == ItemEvent.SELECTED) {
            imageLabel.setIcon(images[idx]);
        }
    });
}
```

핵심 구조는 같습니다.

```java
final int idx = i;
```

이 한 줄이 **각 버튼마다 자기 이미지 번호를 기억하게 만드는 역할**입니다.

---

### ❓ 질문 (User)
```
import java.awt.BorderLayout;
import java.awt.Button;
import java.awt.Color;
import java.awt.Container;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;

import javax.swing.ButtonGroup;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.SwingConstants;

public class Swing0526_8 extends JFrame{
	private JRadioButton[] radio = new JRadioButton[3];
	private String[] text = {"사과", "배", "체리"};
	private ImageIcon[] images = {
			new ImageIcon("images/apple.jpg"),
			new ImageIcon("images/pear.jpg"),
			new ImageIcon("images/cherry.jpg")};
	private JLabel imageLabel = new JLabel();
	
	
	public Swing0526_8() {
		setTitle("라디오 버튼 Item Event 예제");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);	
		Container c = getContentPane();
		c.setLayout(new BorderLayout());
		
		JPanel radioPanel = new JPanel();
		radioPanel.setBackground(Color.GRAY);
		ButtonGroup g = new ButtonGroup();
		
		for (int i = 0; i < radio.length; i++) {
			radio[i] = new JRadioButton(text[i]);
			g.add(radio[i]);
			radioPanel.add(radio[i]);
			radio[i].addItemListener(new ItemListener() {
								
//			final int idx = i;
			
				@Override
				public void itemStateChanged(ItemEvent e) {
//					if (e.getStateChange() == ItemEvent.SELECTED)
//						imageLabel.setIcon(images[idx]);
					if (radio[0].isSelected())
						imageLabel.setIcon(images[0]);
					else if (radio[1].isSelected())
						imageLabel.setIcon(images[1]);
					else 
						imageLabel.setIcon(images[2]);
					
				}
			});
		}
		
		radio[2].setSelected(true);
		c.add(radioPanel, BorderLayout.NORTH);
		c.add(imageLabel, BorderLayout.CENTER);
		imageLabel.setHorizontalAlignment(SwingConstants.CENTER);
		
		setSize(250, 200);
		setVisible(true);
	}

	public static void main(String[] args) {
		new Swing0526_8();

	}

}


이거를 idx 로 해서 for 문에 따라 하고 싶은데, 잘 모르겠어. 알려줘.
