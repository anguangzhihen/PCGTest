using UnityEngine;

public class TestPIp : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
	    Debug.LogError(Vector3.LerpUnclamped(Vector3.one, Vector3.one * 3, 0.2f));
	    Debug.LogError(Vector3.LerpUnclamped(Vector3.one, Vector3.one * 3, 0.6f));
	    Debug.LogError(Vector3.LerpUnclamped(Vector3.one, Vector3.one * 3, 0.8f));
	    Debug.LogError(Vector3.LerpUnclamped(Vector3.one, Vector3.one * 3, 1.3f));
	}

    // Update is called once per frame
    void Update()
    {
        
    }
}
