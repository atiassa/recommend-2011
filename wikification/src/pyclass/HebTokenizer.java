package pyclass;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.Enumeration;
import java.util.Properties;

import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;


public class HebTokenizer {
    private PyObject run_tokenize;
    
    public HebTokenizer() {
        PythonInterpreter interpreter = new PythonInterpreter();
        interpreter.execfile("hebtokenizer.py");
        run_tokenize = interpreter.get("run_tokenize");
    }

    public String tokenize(String text) throws UnsupportedEncodingException {
        PyObject ans = run_tokenize.__call__(new PyString(text));
        return new String(ans.toString().getBytes("ISO-8859-1"), "UTF-8");
    }
	    
}
