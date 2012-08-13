package pyclass;

import java.io.UnsupportedEncodingException;

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

    public void tokenize() throws UnsupportedEncodingException {
        PyObject ans = run_tokenize.__call__(new PyString("in1.txt"),new PyString("out1.txt"));
        //return new String(ans.toString().getBytes("ISO-8859-1"), "UTF-8");
    }
	    
}
