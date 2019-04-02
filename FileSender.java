/*
 * Filename:	FileSender.java
 *
 * Author:		Oxnz
 * Email:		yunxinyi@gmail.com
 * Created:		2016-09-02 18:05:45 CST
 * Last-update:	2016-09-02 18:05:45 CST
 * Description: anchor
 *
 * Version:		0.0.1
 * Revision:	[NONE]
 * Revision history:	[NONE]
 * Date Author Remarks:	[NONE]
 *
 * License: 
 * Copyright (c) 2016 Oxnz
 *
 * Distributed under terms of the [LICENSE] license.
 * [license]
 *
 */

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.OutputStream;
import java.net.Socket;

public class FileSender {
	private static int PORT = 8000;
	private static String ADDR = "192.168.249.247";
	private static String FILE = "/path/to/file";
	private static int BUFSIZ = 1<<20;

    public static void main(String[] args) {
		try {
			File file = new File(FILE);
			FileInputStream fis = new FileInputStream(file);
			BufferedInputStream bis = new BufferedInputStream(fis);
			Socket socket = new Socket(ADDR, PORT);
			System.out.println("connected");
			OutputStream os = socket.getOutputStream();
			byte[] buffer = new byte[BUFSIZ];
			for (int sz = 0; sz != -1; sz = bis.read(buffer)) {
				os.write(buffer, 0, sz);
				System.out.print(".");
			}
			os.flush();
			bis.close();
			fis.close();
			os.close();
			socket.close();
			System.out.println("done");
		} catch (Exception e) {
			e.printStackTrace();
		}
    }
}
