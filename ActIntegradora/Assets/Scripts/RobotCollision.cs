using UnityEngine;

public class RobotCollision : MonoBehaviour
{
    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Robot"))
        {
            Debug.Log("Colision con otro Robot");
        }

        if (other.CompareTag("Caja"))
        {
            Debug.Log("Colision con Caja");
        }
    }

}
