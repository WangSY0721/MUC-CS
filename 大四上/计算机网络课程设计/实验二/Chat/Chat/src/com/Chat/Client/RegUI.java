package com.Chat.Client;

import java.awt.*;

import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.GroupLayout;
import javax.swing.GroupLayout.Alignment;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.LayoutStyle.ComponentPlacement;
import javax.swing.JPasswordField;
import java.awt.event.ActionListener;
import java.io.*;
import java.net.Socket;
import java.net.UnknownHostException;
import java.awt.event.ActionEvent;

public class RegUI extends JDialog {

	private static final long serialVersionUID = 1331039277600772730L;
	private final JPanel contentPanel = new JPanel();
	private JTextField textField;
	private JPasswordField passwordField;
	private JPasswordField passwordField_1;
	private Socket register;
	private PrintWriter send;
	private BufferedReader receive;
	private String ip;

	public static void main(String[] args) {
		try {
			RegUI dialog = new RegUI();
			dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
			dialog.setVisible(true);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public RegUI() {
		setResizable(false);
		setIconImage(Toolkit.getDefaultToolkit().getImage(RegUI.class.getResource("/com/Chat/Client/Chat_ico2.png")));
		setBounds(200, 200, 500, 300);
		setTitle("注册账号");
		getContentPane().setLayout(new BorderLayout());
		contentPanel.setBorder(new EmptyBorder(5, 5, 5, 5));
		getContentPane().add(contentPanel, BorderLayout.CENTER);
		Font font1=new Font("宋体", Font.BOLD, 20);
		JLabel label = new JLabel("昵称   :");
		label.setFont(font1);
		JLabel label_1 = new JLabel("密码   : ");
		label_1.setFont(font1);
		JLabel label_2 = new JLabel("确定密码:");
		label_2.setFont(font1);
		textField = new JTextField();
		textField.setColumns(20);
		passwordField = new JPasswordField();
		passwordField_1 = new JPasswordField();
		GroupLayout gl_contentPanel = new GroupLayout(contentPanel);
		gl_contentPanel
				.setHorizontalGroup(gl_contentPanel.createParallelGroup(Alignment.LEADING)
						.addGroup(gl_contentPanel.createSequentialGroup().addContainerGap()
								.addGroup(gl_contentPanel.createParallelGroup(Alignment.LEADING)
										.addGroup(gl_contentPanel.createSequentialGroup()
												.addComponent(label, GroupLayout.PREFERRED_SIZE, 100,
														GroupLayout.PREFERRED_SIZE)
												.addPreferredGap(ComponentPlacement.RELATED).addComponent(textField,
														GroupLayout.PREFERRED_SIZE, 300, GroupLayout.PREFERRED_SIZE))
						.addGroup(gl_contentPanel.createSequentialGroup().addComponent(label_2)
								.addPreferredGap(ComponentPlacement.RELATED).addComponent(passwordField_1,
										GroupLayout.PREFERRED_SIZE, 300, GroupLayout.PREFERRED_SIZE))
						.addGroup(gl_contentPanel.createSequentialGroup().addComponent(label_1)
								.addPreferredGap(ComponentPlacement.RELATED).addComponent(passwordField,
										GroupLayout.PREFERRED_SIZE, 300, GroupLayout.PREFERRED_SIZE)))
						.addContainerGap(150, Short.MAX_VALUE)));
		gl_contentPanel.setVerticalGroup(gl_contentPanel.createParallelGroup(Alignment.LEADING).addGroup(gl_contentPanel
				.createSequentialGroup().addGap(29)
				.addGroup(gl_contentPanel.createParallelGroup(Alignment.BASELINE).addComponent(label).addComponent(
						textField, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
				.addGap(39)
				.addGroup(gl_contentPanel.createParallelGroup(Alignment.BASELINE).addComponent(label_1).addComponent(
						passwordField, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE,
						GroupLayout.PREFERRED_SIZE))
				.addGap(29)
				.addGroup(gl_contentPanel.createParallelGroup(Alignment.BASELINE).addComponent(label_2).addComponent(
						passwordField_1, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE,
						GroupLayout.PREFERRED_SIZE))
				.addContainerGap(76, Short.MAX_VALUE)));
		contentPanel.setLayout(gl_contentPanel);
		{
			JPanel buttonPane = new JPanel();
			buttonPane.setLayout(new FlowLayout(FlowLayout.RIGHT));
			getContentPane().add(buttonPane, BorderLayout.SOUTH);
			{
				Font font = new Font("宋体", Font.BOLD, 15);
				JButton okButton = new JButton("注册");
				okButton.setFont(font);
				okButton.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						if ((passwordField.getPassword().length>0)&&new String(passwordField.getPassword()).equals(new String(passwordField_1.getPassword()))) {
							try {
								register = new Socket(ip, 34343);
								System.out.println("开始注册");
								register();
							} catch (UnknownHostException e1) {
								e1.printStackTrace();
							} catch (IOException e1) {
								e1.printStackTrace();
							}
						} else {
							Dialog exError = new Dialog(RegUI.this, "验证错误", true);
							exError.add(new Label("请确定两次输入的密码是否正确！"));
							exError.setBounds(600, 200, 180, 100);
							exError.setLayout(new FlowLayout());
							JButton exButton = new JButton("确定");
							exError.add(exButton);
							exButton.addActionListener(new ActionListener() {
								public void actionPerformed(ActionEvent e) {
									exError.dispose();
								}
							});
							exError.setVisible(true);
						}

					}
				});
				okButton.setActionCommand("OK");
				buttonPane.add(okButton);
				getRootPane().setDefaultButton(okButton);
			}
			{
				Font font = new Font("宋体", Font.BOLD, 15);

				JButton cancelButton = new JButton("重置");
				cancelButton.setFont(font);
				cancelButton.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						textField.setText("");
						passwordField.setText("");
						passwordField_1.setText("");
					}
				});
				cancelButton.setActionCommand("Cancel");
				buttonPane.add(cancelButton);
			}
		}

	}

	public RegUI(String ip) {
		this();
		this.ip = ip;

	}

	public void register() {
		try {
			send = new PrintWriter(register.getOutputStream(), true);// 发送信息，且刷新
			receive = new BufferedReader(new InputStreamReader(register.getInputStream()));
			String name = textField.getText();
			String password = new String(passwordField.getPassword());
			send.println(name);
			send.println(password);
			String info = receive.readLine();
			switch (info) {
			case "Exist":
				Dialog exError = new Dialog(this, "用户已存在", true);
				exError.add(new Label("用户已存在，请尝试其他帐号"));
				exError.setBounds(600, 200, 280, 100);
				exError.setLayout(new FlowLayout());
				JButton exButton = new JButton("确定");
				exError.add(exButton);
				exButton.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						exError.dispose();
					}
				});
				exError.setVisible(true);
				break;
			case "RegisterSuccess":
				Dialog reS = new Dialog(this, "注册成功", true);
				reS.add(new Label("恭喜您，注册成功！"));
				reS.setBounds(600, 200, 280, 100);
				reS.setLayout(new FlowLayout());
				JButton reSButton = new JButton("确定");
				reS.add(reSButton);
				reSButton.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						reS.dispose();
						RegUI.this.dispose();
					}
				});
				reS.setVisible(true);
				break;
			default:
				break;
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}
