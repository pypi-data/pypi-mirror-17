package python.platform;

import java.lang.management.ManagementFactory;
import java.lang.management.ThreadMXBean;


public class JavaPlatform implements python.Platform {
    private org.python.stdlib._io.TextIOWrapper _stderr;
    private org.python.stdlib._io.TextIOWrapper _stdout;
    private org.python.stdlib._io.TextIOWrapper _stdin;

    public JavaPlatform() {
        _stderr = new org.python.stdlib._io.TextIOWrapper(System.err);
        _stdout = new org.python.stdlib._io.TextIOWrapper(System.out);
        _stdin = new org.python.stdlib._io.TextIOWrapper(System.in);
    }

    public long clock() {
        ThreadMXBean tmxb = ManagementFactory.getThreadMXBean();
        return tmxb.getCurrentThreadCpuTime();
    }

    public void debug(java.lang.String msg) {
        System.out.println("DEBUG " + msg);
    }

    public void debug(java.lang.String msg, java.lang.Object obj) {
        System.out.println("DEBUG " + msg + ": " + obj);
    }

    public org.python.Object stderr() {
        return _stderr;
    }

    public org.python.Object stdout() {
        return _stdout;
    }

    public org.python.Object stdin() {
        return _stdin;
    }
}