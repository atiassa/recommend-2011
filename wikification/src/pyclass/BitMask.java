package pyclass;

import java.io.UnsupportedEncodingException;

import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;

public class BitMask {
	 private PyObject run;
	    
	    public BitMask() {
	        PythonInterpreter interpreter = new PythonInterpreter();
	        interpreter.execfile("bitmasks_to_tags.py");
	        run = interpreter.get("run");
	    }

	    public String tokenize(String text) throws UnsupportedEncodingException {
	        PyObject ans = run.__call__(new PyString(text));
	        return new String(ans.toString().getBytes("ISO-8859-1"), "UTF-8");
	    }
}
