package com.Chat.Server;

import java.io.*;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 * 公共离线留言工具类：保存公共离线通知，所有新上线用户均可查看
 */
public class OfflineMessageUtil {
    // 公共离线留言存储文件路径
    private static final String OFFLINE_FILE = "D:\\public_offline_messages.txt";
    private static final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

    /**
     * 保存公共离线留言（发送方+内容+时间）
     * @param sender 发送方用户名
     * @param content 留言内容
     */
    public static void savePublicOfflineMessage(String sender, String content) {
        File file = new File(OFFLINE_FILE);
        if (!file.exists()) {
            try {
                file.createNewFile();
            } catch (IOException e) {
                e.printStackTrace();
                return;
            }
        }

        // 追加写入公共留言
        try (PrintWriter out = new PrintWriter(new FileWriter(file, true))) {
            String time = sdf.format(new Date());
            // 格式：发送方::内容::时间戳
            out.println(sender + "::" + content + "::" + time);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * 读取所有公共离线留言（读取后清空，避免重复推送）
     * @return 离线留言列表（所有用户共用）
     */
    public static List<String> getPublicOfflineMessages() {
        List<String> messages = new ArrayList<>();
        File file = new File(OFFLINE_FILE);
        if (!file.exists()) {
            return messages;
        }

        // 读取所有留言
        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] parts = line.split("::", 3);
                if (parts.length == 3) {
                    // 拼接格式：【公共离线通知】发送方 (时间)：内容
                    String msg = "【公共离线通知】" + parts[0] + " (" + parts[2] + ")：" + parts[1];
                    messages.add(msg);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        // 读取后清空文件（避免重复推送）
        file.delete();
        return messages;
    }
}